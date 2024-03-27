from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'  # Replace with your database URI
db = SQLAlchemy(app)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

@app.route('/')
def index():
    return render_template('create_quiz.html')

@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    title = request.form['title']
    description = request.form['description']
    time_limit = request.form['time_limit']
    questions = request.form.getlist('questions[]')
    options = request.form.getlist('options[]')
    correct_answers = request.form.getlist('correct_answer[]')

    # Validate form data
    if not title or not description or not time_limit or not questions or not options or not correct_answers:
        return "Please fill out all fields."

    # Create Quiz object
    quiz = Quiz(title=title, description=description, time_limit=int(time_limit))
    db.session.add(quiz)
    db.session.commit()

    # Create questions and options
    for i, question_text in enumerate(questions):
        question = Question(question_text=question_text, quiz_id=quiz.id)
        db.session.add(question)
        db.session.commit()

        # Add options for each question
        for j, option_text in enumerate(options[i*4:i*4+4]):
            is_correct = True if j == int(correct_answers[i]) else False
            option = Option(option_text=option_text, is_correct=is_correct, question_id=question.id)
            db.session.add(option)
            db.session.commit()

    return "Quiz created successfully!"

if __name__ == '__main__':
    app.run(debug=True)
