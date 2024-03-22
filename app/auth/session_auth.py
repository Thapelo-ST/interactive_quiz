#!/usr/bin/env python3
"""
validate without overlay, switch environment variables
"""
import os
import uuid
from flask import app, jsonify, request
from app.models import User
from auth import Auth


class SessionAuth(Auth):
    """
    validate without overlay, switch environment variables
    """
    user_id_by_session_id = {}

    """ creates a session ID"""
    def create_session(self, user_id: str = None) -> str:
        """ creates a session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if request is None:
            return None

        cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name)

    """returns a user id based on a session id"""
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id based on a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    """returns the user instance based on a cookie value"""
    def current_user(self, request=None):
        """returns the user instance based on a cookie value"""
        if request is None:
            return None

        session_id = self.session_cookie(request)

        if session_id:
            user_id = self.user_id_for_session_id(session_id)

            if user_id:
                user = User.get(user_id)
                return user

    @app.route('/auth_session/login', methods=['POST'],
                     strict_slashes=False)
    def session_login():
        """Handles user authentication using Session ID"""
        from auth import auth
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})

        if not user:
            return jsonify({"error": "no user found for this email"}), 404

        if not user[0].is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user[0].id)

        response_data = user[0].to_json()

        cookie_name = app.config.get("SESSION_NAME", "_my_session_id")
        response_data["cookie"] = {cookie_name: session_id}

        return jsonify(response_data)
