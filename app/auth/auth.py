import os
import bcrypt
from uuid import uuid4
from flask import request
from app.user.users import User
from app.db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

class Auth:
    """Manages API authentication"""

    def __init__(self, db):
        self._db = db

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Check if authentication is required for a given path"""
        if not path or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self) -> str:
        """Get the Authorization header"""
        return request.headers.get('Authorization')

    def current_user(self) -> User:
        """Get the current authenticated user"""
        session_id = self.session_cookie()

        if session_id:
            user_id = self.user_id_for_session_id(session_id)

            if user_id:
                return self._db.get_user(user_id)

    def session_cookie(self) -> str:
        """Get the session ID from the request's cookies"""
        cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name)

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")

        hashed_password = self._hash_password(password)
        return self._db.add_user(email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user"""
        user = self._db.find_user_by(email=email)

        if user:
            session_id = str(uuid4())
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User or None: # type: ignore
        """Get user from session ID"""
        if session_id:
            return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token"""
        user = self._db.find_user_by(email=email)

        if user:
            reset_token = str(uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        raise ValueError(f"User with email {email} not found")

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update user's password using reset token"""
        user = self._db.find_user_by(reset_token=reset_token)

        if user:
            hashed_password = self._hash_password(new_password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        else:
            raise ValueError("Invalid reset token")

    def _hash_password(self, password: str) -> bytes:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

db_instance = DB("sqlite:///database.db")
AUTH = Auth(db_instance)
# if there is a circular imports error fix here