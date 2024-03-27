from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.quiz.models import Option, Question, Quiz, QuizAttempt
from app.user.users import User
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

class DB:
    """DB class for database operations"""

    def __init__(self, db_uri):
        """Initialize a new DB instance"""
        self.engine = create_engine(db_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.__session = None

    @property
    def db_session(self):
        """Property to access the session"""
        if self.__session is None:
            self.__session = self.Session()
        return self.__session

    def create_all(self):
        """Create all tables"""
        User.metadata.create_all(self.engine)
        Question.metadata.create_all(self.engine)
        Option.metadata.create_all(self.engine)
        QuizAttempt.metadata.create_all(self.engine)
        Quiz.metadata.create_all(self.engine) 

    # USERS 
    def add_user(self, email, hashed_password):
        """Add a new user to the database"""
        session = self.Session()
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        session.close()
        return new_user

    def find_user_by_email(self, email):
        """Find a user by email"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(email=email).one()
        except NoResultFound:
            user = None
        session.close()
        return user

    def update_user(self, user_id, **kwargs):
        """Update user attributes"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).one()
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")
        finally:
            session.close()

    def delete_user(self, user_id):
        """Delete a user from the database by user ID"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).one()
            session.delete(user)
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}")
        finally:
            session.close()

    def change_password(self, user_id, new_password):
        """Change user's password"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).one()
            user.password = new_password
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}")
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        """Retrieve a user from the database by user ID"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).one()
            return user
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}")
        finally:
            session.close()

    def get_all_users(self):
        """Retrieve all users from the database"""
        session = self.Session()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()

    # QUIZ
    def create_quiz(self, quiz_data):
        """Create a new quiz in the database"""
        session = self.Session()
        try:
            new_quiz = Quiz(**quiz_data)
            session.add(new_quiz)
            session.commit()
            return new_quiz
        finally:
            session.close()

    def update_quiz(self, quiz_id, quiz_data):
        """Update an existing quiz in the database"""
        session = self.Session()
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).one()
            for key, value in quiz_data.items():
                setattr(quiz, key, value)
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"No quiz found with id {quiz_id}")
        finally:
            session.close()

    def delete_quiz(self, quiz_id):
        """Delete a quiz from the database"""
        session = self.Session()
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).one()
            session.delete(quiz)
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"No quiz found with id {quiz_id}")
        finally:
            session.close()

    def get_quiz_by_id(self, quiz_id):
        """Retrieve a quiz from the database by quiz ID"""
        session = self.Session()
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).one()
            return quiz
        except NoResultFound:
            raise NoResultFound(f"No quiz found with id {quiz_id}")
        finally:
            session.close()

    def get_all_quizzes(self):
        """Retrieve all quizzes from the database"""
        session = self.Session()
        try:
            quizzes = session.query(Quiz).all()
            return quizzes
        finally:
            session.close()

    def get_quizzes_by_user(self, user_id):
        """Retrieve quizzes created by a specific user"""
        session = self.Session()
        try:
            quizzes = session.query(Quiz).filter_by(user_id=user_id).all()
            return quizzes
        finally:
            session.close()

    def add_question_to_quiz(self, quiz_id, question_data):
        """Add a new question to an existing quiz"""
        session = self.Session()
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).one()
            new_question = Question(**question_data)
            quiz.questions.append(new_question)
            session.commit()
            return new_question
        except NoResultFound:
            raise NoResultFound(f"No quiz found with id {quiz_id}")
        finally:
            session.close()

    def remove_question_from_quiz(self, quiz_id, question_id):
        """Remove a question from a quiz"""
        session = self.Session()
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).one()
            question = session.query(Question).filter_by(id=question_id).one()
            quiz.questions.remove(question)
            session.commit()
        except NoResultFound:
            raise NoResultFound("No quiz or question found with the provided IDs")
        finally:
            session.close()

    def submit_quiz_attempt(self, quiz_attempt_data):
        """Record a user's attempt at taking a quiz"""
        session = self.Session()
        try:
            new_quiz_attempt = QuizAttempt(**quiz_attempt_data)
            session.add(new_quiz_attempt)
            session.commit()
            return new_quiz_attempt
        finally:
            session.close()

    def get_quiz_attempts_by_user(self, user_id):
        """Retrieve all quiz attempts made by a specific user"""
        session = self.Session()
        try:
            quiz_attempts = session.query(QuizAttempt).filter_by(user_id=user_id).all()
            return quiz_attempts
        finally:
            session.close()
