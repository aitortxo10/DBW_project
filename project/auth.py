from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from .models import Challenge
from . import db
from email_validator import validate_email, EmailNotValidError

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember=True if request.form.get('remember') else False

    user=User.query.filter_by(email=email).first()#Load the information related to the user

    if not user or not check_password_hash(user.password,password): #If the password or the email is not correct, flash an error message and redirectonce more to the login page
        flash('Incorrect user or password, please try again')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile')) #If the login info is correct, load the profile of the user

@auth.route('/signup/')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    #First extract all the data from the signup form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Email validation with email_validator package
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e: # if email not valid (not following name@example.com), then redirect to signup with error message
        flash(str(e))
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first() # Check if a user with such email already exists

    if user: # If a user is found redirect once again to the signup page with the corresponding message
        flash('Email address already exists. ')
        # instead of redirecting, use render_template that allows to pass variables to jinja
        return render_template('signup.html', var="auth.login" )

    new_user=User(email=email, name=name, password=generate_password_hash(password,method='sha256')) #Create a new User class instance with the new data inputted
    db.session.add(new_user)#Add the user to the database
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/exercises')
@login_required
def exercises():
    exercise_list = Challenge.query.all()
    return render_template('exercises.html', data=exercise_list)
