#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth
from base64 import b64decode
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication mechanism class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 Authorization header """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        h_list = authorization_header.split()
        if h_list[0] != 'Basic':
            return None
        return h_list[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode base64 authorization header """
        b64_h = base64_authorization_header
        if b64_h is None:
            return None
        if type(b64_h) != str:
            return None

        try:
            decoded = b64decode(b64_h)
        except base64.binascii.Error:
            return None

        try:
            decoded = decoded.decode('utf-8')
        except UnicodeDecodeError:
            decoded = None
        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract user's credentials from auth header """
        dcd_b64_h = decoded_base64_authorization_header
        if dcd_b64_h is None:
            return (None, None)
        if type(dcd_b64_h) is not str:
            return (None, None)

        credentials = dcd_b64_h.split(':')
        if len(credentials) < 2:
            return (None, None)
        return (credentials[0], ":".join(credentials[1:]))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ return the User instance based on his email and pwd """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        s_result = User.search({"email": user_email})
        if len(s_result) == 0:
            return None

        user = s_result[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ log a user in """
        if request is None:
            return None
        extracted_auth_header = None
        decoded_auth_header = None
        user_credentials = None
        user = None
        auth_header = self.authorization_header(request)
        if auth_header:
            extracted_auth_header = self.extract_base64_authorization_header(
                                    auth_header)
        if extracted_auth_header:
            decoded_auth_header = self.decode_base64_authorization_header(
                                  extracted_auth_header)
        if decoded_auth_header:
            user_credentials = self.extract_user_credentials(
                               decoded_auth_header)
        if user_credentials:
            user = self.user_object_from_credentials(*user_credentials)
        if user:
            return user
        return None
