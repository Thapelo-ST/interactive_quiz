from flask import Flask
from app.auth.routes import auth_bp
from app.quiz.routes import quiz_bp
from app.user.routes import user_blueprint
from app.db import DB

# Create Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(user_blueprint)

# Initialize the database
db_instance = DB("sqlite:///path/to/database.db")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
