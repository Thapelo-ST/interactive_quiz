from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserEnum(Enum):
    ADMIN = 'admin'
    CLIENT = 'client'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserEnum.ADMIN, UserEnum.CLIENT), nullable=False, default=UserEnum.CLIENT)

class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="quizzes")
    time_limit = Column(Integer)
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship('QuizAttempt', back_populates='quiz')
    # user_attempts = relationship("QuizAttempt", order_by=QuizAttempt.id, back_populates="quiz")


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")

class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_correct = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="options")


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    score = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    # quiz_attempts = relationship("Quiz", back_populates="user_attempts")



User.quizzes = relationship("Quiz", order_by=Quiz.id, back_populates="user")
Quiz.user_attempts = relationship("QuizAttempt", order_by=QuizAttempt.id, back_populates="quiz", overlaps="attempts")
# User.quiz_attempts = relationship("QuizAttempt", order_by=QuizAttempt.id, back_populates="user")
User.quiz_attempts = relationship("QuizAttempt", order_by=QuizAttempt.id, back_populates="user", overlaps="user_attempts")
Question.options = relationship("Option", order_by=Option.id, back_populates="question")
