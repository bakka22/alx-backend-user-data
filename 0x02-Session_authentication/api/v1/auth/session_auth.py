#!/usr/bin/env python3
""" session authentication """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ session authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a new session """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid4()
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id
