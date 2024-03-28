import hashlib
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from sqlalchemy_utils import ChoiceType
from app.models import Base

class UserEnum(Enum):
    ADMIN = 'admin'
    CLIENT = 'client'

class UserModel(Base):
    """ User class
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    _password = Column('password', String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserEnum.ADMIN, UserEnum.CLIENT), nullable=False, default=UserEnum.CLIENT)

    def __init__(self, email, password, role=UserEnum.CLIENT, first_name=None, last_name=None):
        """ Initialize a User instance
        """
        self.email = email
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or not isinstance(pwd, str):
            raise ValueError("Password must be a string")
        self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def save(self):
        """ Save user to database """
        from app.db import db_session
        db_session.add(self)
        db_session.commit()
        db_session.close()

    @classmethod
    def get_by_email(cls, email):
        """ Get user by email """
        from app.db import db_session
        return db_session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, user_id):
        """ Get user by id """
        from app.db import db_session
        return db_session.query(cls).filter_by(id=user_id).first()
