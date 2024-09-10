#!/usr/bin/env python3
""" authentication module """
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ hash a password into bytes """
    salt = gensalt()
    return hashpw(bytes(password, "utf-8"), salt)
