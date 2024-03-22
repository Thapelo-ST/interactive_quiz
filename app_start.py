"""
flask app
"""
from flask import Flask, Response, abort, jsonify, make_response, request, redirect
from app.auth.auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> jsonify:
    """Home page."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def users() -> jsonify:
    """ Create a new user and returns it with an assigned token."""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        AUTH.register_user(email, password)

        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """ logs in the user and creates a session id """
    email = request.form.get('email')
    password = request.form.get('password')

    session_id = None
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response_data = {"email": email, "message": "logged in"}
            response = make_response(jsonify(response_data))
            response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """Logs out the user and destroys the session."""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            AUTH.destroy_session(user.id)
            response = make_response(redirect('/'))
            response.delete_cookie('session_id')
            return response

    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> jsonify:
    """Returns user profile information."""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            response_data: dict = {"email": user.email}
            return jsonify(response_data), 200

    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Generates and responds with a reset password token."""
    try:
        email = request.form.get('email')

        user = AUTH.get_user_by_email(email)
        if not user:
            abort(403, "Email not registered")

        reset_token = AUTH.get_reset_password_token(email)

        response_data = {"email": email, "reset_token": reset_token}
        return jsonify(response_data), 200

    except Exception as e:
        abort(500, str(e))


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update user's password using reset_token."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        response_data = {"email": email, "message": "Password updated"}
        return jsonify(response_data), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
