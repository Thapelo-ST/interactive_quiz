from flask import Blueprint, request, jsonify
from app.auth.auth import AUTH

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'message': f'Registration successful for {email}'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            return jsonify({'session_id': session_id}), 200
        else:
            return jsonify({'error': 'Failed to create session'}), 500
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session_id = request.headers.get('Authorization')
    if session_id:
        AUTH.destroy_session(session_id)
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        # Send reset token via email or any other preferred method
        return jsonify({'message': 'Reset password token generated'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@auth_bp.route('/update-password', methods=['POST'])
def update_password():
    data = request.json
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
