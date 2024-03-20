from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class User(Document):
    """
    User model to represent users of the application.
    """
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

class Quiz(Document):
    """
    Quiz model to represent quizzes in the application.
    """
    title = StringField(required=True)
    questions = ListField(ReferenceField('Question'))
    time_for_quiz = DateTimeField()

class Question(Document):
    """
    Question model to represent questions within quizzes.
    """
    text = StringField(required=True)
    options = ListField(StringField())
    correct_answer = StringField(required=True)

class Response(Document):
    """
    Response model to represent user responses to quiz questions.
    """
    user = ReferenceField('User')
    quiz = ReferenceField('Quiz')
    question = ReferenceField('Question')
    selected_option = StringField()
