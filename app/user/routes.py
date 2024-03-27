from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.user.users import User, UserEnum
# from app.db import db_session

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Check if user already exists
        if User.get_by_email(email):
            flash('Email already exists. Please choose another one.', 'error')
            return redirect(url_for('user.register'))

        # Create a new user
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.get_by_email(email)
        if user and user.is_valid_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index')) 

        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('user.login'))

    return render_template('login.html')

@user_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
