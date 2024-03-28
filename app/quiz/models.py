from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models import Base

class QuizModel(Base):
    """Model for storing quizzes"""
    __tablename__ = 'quizzes'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    time_limit = Column(Integer)  # Time limit for completing the quiz in minutes
    questions = relationship('Question', back_populates='quiz')
    attempts = relationship('QuizAttempt', back_populates='quiz')

class QuestionModel(Base):
    """Model for storing questions"""
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    question_text = Column(String(255), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    quiz = relationship('Quiz', back_populates='questions')
    options = relationship('Option', back_populates='question')

class OptionModel(Base):
    """Model for storing options for multiple-choice questions"""
    __tablename__ = 'options'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    option_text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='options')

class QuizAttemptModel(Base):
    """Model for storing quiz attempts"""
    __tablename__ = 'quiz_attempts'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    quiz = relationship('Quiz', back_populates='attempts')
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming you have a User model
    score = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
