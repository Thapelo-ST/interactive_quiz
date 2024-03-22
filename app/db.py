#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from app.models import Base, User


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

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database"""
        if email is None and hashed_password is None:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ find user function """
        users = self._session.query(User)
        found_user = None
        """for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            found_user = None
            for user in users:
                if getattr(user, key) == value:
                    if found_user is not None:
                        raise InvalidRequestError
                    found_user = user
            if found_user is not None:
                return found_user
        raise NoResultFound"""
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in users:
                if getattr(user, key) == value:
                    if found_user is not None:
                        raise InvalidRequestError
                    found_user = user

        if found_user is not None:
            return found_user

        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes in the database"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError("Invalid attribute: {}".format(key))
            self._session.commit()

        except NoResultFound:
            raise NoResultFound("No user found with id {}".format(user_id))
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")