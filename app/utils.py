from flask import session, redirect, url_for

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

def get_current_user():
    """
    Retrieve the current logged-in user based on their user ID stored in the session.
    """
    from app.models import User  # Import inside function to avoid circular import

    user_id = session.get('user_id')
    if user_id:
        return User.objects(id=user_id).first()

def require_login(func):
    """
    Decorator to require login for accessing certain routes.
    Redirects to the login page if the user is not logged in.
    """
    from functools import wraps
    from flask import flash

    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper
