import os
import bcrypt
from uuid import uuid4
from flask import request
from app.models import User
from app.db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

class Auth:
    """Manages API authentication"""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Returns false paths and executed paths"""
        if not path or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self) -> str:
        """Responsible for auth header"""
        if 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self) -> User:
        """Returns current user"""
        if request is None:
            return None

        session_id = self.session_cookie(request)

        if session_id:
            user_id = self.user_id_for_session_id(session_id)

            if user_id:
                user = User.get(user_id)
                return user

    def session_cookie(self):
        """Returns a cookie value from a request"""
        cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name)

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and returns a User object"""
        hashed_password = self._hash_password(password)
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Logs in an existing user and returns a User object if successful."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Generates a session id from a given email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = str(uuid4())
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User or None: # type: ignore
        """Returns the corresponding User for a given session ID, or None if not found."""
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates and returns a reset password token for the user."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"User with email {email} not found")

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Updates user's password using reset_token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(new_password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")

    def _hash_password(self, password: str) -> bytes:
        """Hashes the provided password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)
