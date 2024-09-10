#!/usr/bin/env python3
""" authentication module """
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash a password into bytes """
    salt = gensalt()
    return hashpw(bytes(password, "utf-8"), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user in database """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        if user:
            raise ValueError(f"user {user.email} already exists")
        hashedpw = _hash_password(password)
        user = self._db.add_user(email, hashedpw)
        return user
