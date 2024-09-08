#!/usr/bin/env python3
""" session authentication """
from api.v1.auth.auth import Auth
import os
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ session authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a new session for user """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user_id for a session id """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ return User instance based on cookie value """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        usr_id = self.user_id_for_session_id(session_id)
        if usr_id is None:
            return None
        return User.get(usr_id)

    def destroy_session(self, request=None):
        """ destroy user's session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        usr_id = self.user_id_for_session_id(session_id)
        if usr_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
