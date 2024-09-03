#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth
from base64 import b64decode
import base64


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

        return decoded.decode('utf-8')
