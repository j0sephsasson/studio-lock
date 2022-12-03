
from flask import Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask.templating import render_template
from .db_models import User
from . import db
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login_post', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page w/ flash

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup_post', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user_email_check = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user_username_check = User.query.filter_by(email=email).first() # if this returns a user, then the username already exists in database

    if user_email_check: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if user_username_check: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create a new user for the user table. Hash the password so the plaintext version isn't saved.
    new_user = User(name=name, username=username, email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Account Created!')  ## successful signup alert

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
