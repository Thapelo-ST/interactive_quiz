from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_session import Session
import redis
from app.auth import login_required
from app.models import User

# Create Flask application instance
app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Initialize MongoEngine for MongoDB connection
db = MongoEngine(app)

# Initialize Flask-Session for session management
Session(app)

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

# Register blueprints for organizing routes and views
from app.routes import auth_bp, quiz_bp
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)

# Import routes after app creation to avoid circular imports
from app import routes
