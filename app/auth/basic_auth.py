#!/usr/bin/env python3
""" Basic authentication class """
from flask import request
from typing import List, Tuple, TypeVar
from auth.auth import Auth
from models import User
import base64


class BasicAuth(Auth):
    """ Basic authentication class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns base64 part of auth header """
        if authorization_header is None\
            or not isinstance(authorization_header, str)\
                or not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """ decodes date from base64 encoding """
        if base64_authorization_header is None\
           or not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_byt = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_byt.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """ Returns user email and password from base64 decoded value """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None

        credentials = tuple(decoded_base64_authorization_header.split(":", 1))
        if len(credentials) != 2:
            return None, None

        return credentials

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'): # type: ignore
        """  Create a User object with the provided credentials """
        if user_email is None or user_pwd is None or\
           not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Overloads auth and retrieves the User instance for a request """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_auth_header is None:
            return None

        user_credentials = self.extract_user_credentials(decoded_auth_header)
        if user_credentials is None:
            return None

        user_email, user_pwd = user_credentials
        return self.user_object_from_credentials(user_email, user_pwd)
