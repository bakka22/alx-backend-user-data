#!/usr/bin/env python3
""" manage Authentication """
from typing import List, TypeVar
import re
import os


class Auth():
    """ authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if a path requires authentication """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"

        for pa in excluded_paths:
            if pa[-1] == "*":
                pa = pa[:-1] + ".*"
                match = re.match(pa, path)
                if match:
                    return False
            elif path == pa:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ return the value of the header request Authorization """
        if request is None:
            return None
        auth_header = request.headers.get("Authorization", None)
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None """
        return None

    def session_cookie(self, request=None):
        """ return a cookie value from a request """
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        if cookie_name:
           return request.cookies.get(cookie_name)
        return None
