#!/usr/bin/env pytho3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password,
                 session_id=None, reset_token=None):
        """ add a user to database """
        new_user = User(email=email, hashed_password=hashed_password,
                        session_id=session_id, reset_token=reset_token)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """ find user by filter """
        for key in kwargs.keys():
            try:
                getattr(User, key)
            except AttributeError:
                raise InvalidRequestError

        users = self._session.query(User).filter_by(**kwargs).all()
        if len(users) == 0:
            raise NoResultFound
        return users[0]
