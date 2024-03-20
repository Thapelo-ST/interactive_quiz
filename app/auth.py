from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User

def login_required(role=None):
    """
    Decorator to require login for accessing certain routes.
    Optionally, specify the required role to access the route.
    Redirects to the login page if the user is not logged in or does not have the required role.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                flash('You must be logged in to access this page.', 'error')
                return redirect(url_for('login'))
            if role and user.role != role:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """
    Retrieve the current logged-in user based on their user ID stored in the session.
    """
    user_id = session.get('user_id')
    if user_id:
        return User.objects(id=user_id).first()

def login_user(user):
    """
    Log in the user by setting their user ID in the session.
    """
    session['user_id'] = str(user.id)

def logout_user():
    """
    Log out the user by removing their user ID from the session.
    """
    session.pop('user_id', None)
