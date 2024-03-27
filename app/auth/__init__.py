# app/auth/__init__.py

# Import the Auth class and any other modules you may need
from app.db import DB
from .auth import Auth

db_instance = DB("sqlite:///path/to/database.db")
AUTH = Auth(db_instance)
