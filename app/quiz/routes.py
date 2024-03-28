from flask import Blueprint, jsonify, request, abort
from app.db import DB
from app.models import Quiz as quiZ

# Create a Blueprint for quiz routes
quiz_bp = Blueprint('quiz_bp', __name__)

# Initialize the database
db = DB("sqlite:////database.db")

@quiz_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz."""
    data = request.json

    # Validate request data
    if not all(key in data for key in ['title', 'user_id', 'time_limit', 'questions']):
        abort(400, 'Incomplete data')

    # Create quiz object
    quiz = quiZ(title=data['title'], user_id=data['user_id'], time_limit=data['time_limit'])

    # Add quiz to database
    db.db_session.add(quiz)
    db.db_session.commit()

    return jsonify({'message': 'Quiz created successfully', 'quiz_id': quiz.id}), 201

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Retrieve a quiz by ID."""
    quiz = db.db_session.query(quiZ).filter_by(id=quiz_id).first()
    if not quiz:
        abort(404, 'Quiz not found')

    # Serialize quiz object and return
    quiz_data = {
        'id': quiz.id,
        'title': quiz.title,
        'user_id': quiz.user_id,
        'time_limit': quiz.time_limit,
        # Add more fields as needed
    }

    return jsonify(quiz_data), 200

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    """Update an existing quiz."""
    data = request.json

    # Get the quiz from the database
    quiz = db.db_session.query(quiZ).filter_by(id=quiz_id).first()
    if not quiz:
        abort(404, 'Quiz not found')

    # Update quiz attributes
    for key, value in data.items():
        setattr(quiz, key, value)

    # Commit changes to the database
    db.db_session.commit()

    return jsonify({'message': 'Quiz updated successfully'}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete a quiz by ID."""
    # Get the quiz from the database
    quiz = db.db_session.query(quiZ).filter_by(id=quiz_id).first()
    if not quiz:
        abort(404, 'Quiz not found')

    # Delete the quiz
    db.db_session.delete(quiz)
    db.db_session.commit()

    return jsonify({'message': 'Quiz deleted successfully'}), 200
