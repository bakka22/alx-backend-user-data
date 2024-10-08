#!/usr/bin/env python3
""" authentication module """
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ hash a password into bytes """
    salt = gensalt()
    return hashpw(bytes(password, "utf-8"), salt)


def _generate_uuid() -> str:
    """ generate uuid """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validate user credintials from login """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ create a new session for user """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ return the user of a session """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """  destroy a user's session """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ set a user's reset_token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = _generate_uuid()
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ update a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        user.hashed_password = _hash_password(password)
        user.reset_token = None
