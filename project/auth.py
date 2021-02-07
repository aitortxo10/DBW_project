from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/signup', methods=['POST'])
def signup_post():                                  #First extract all the data from the signup form
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # Check if a user with such email already exists

    if user:                                         #If a user is found redirect once again to the signup page with the corresponding message
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user=User(email=email, name=name, password=generate_password_hash(password,method='sha256')) #Create a new User class instance with the new data inputted
    db.session.add(new_user)#Add the user to the database
    db.session.commit()

    return redirect(url_for('auth.login'))
