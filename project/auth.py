from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from . import db
from email_validator import validate_email, EmailNotValidError
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember=True if request.form.get('remember') else False

    user=Users.query.filter_by(email=email).first()#Load the information related to the user

    if not user:
        flash('User not registered, please go to sign up')
        return redirect(url_for('auth.login'))
    elif not check_password_hash(user.password,password): #If the password or the email is not correct, flash an error message and redirectonce more to the login page
        flash('Incorrect password, please try again')
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

    user = Users.query.filter_by(email=email).first() # Check if a user with such email already exists

    if user: # If a user is found redirect once again to the signup page with the corresponding message
        flash('Email address already exists. ')
        # instead of redirecting, use render_template that allows to pass variables to jinja
        return render_template('signup.html', var="auth.login" )

    new_user=Users(email=email, name=name, password=generate_password_hash(password,method='sha256')) #Create a new users class instance with the new data inputted
    db.session.add(new_user)#Add the user to the database
    db.session.commit()

    login_user(new_user, remember=True)
    return redirect(url_for('main.profile'))

@auth.route('/exercises')
def exercises():
    exercise_list = Challenges.query.join(LanguagesChallenges).join(ProgrammingLanguages)

    return render_template('exercises.html', exercise_list=exercise_list)

@auth.route('/detailed_exercise/<id>/<language>')
@login_required
def detailed_exercise(id, language):
    # use info from the url instead of a request form
    id=id
    language=language
    challenge=Challenges.query.filter_by(id=id).first()
    return render_template('detailed_exercise.html',challenge=challenge, id=id, language=language)

@auth.route('/test', methods=['POST'])
def testing():
    # we have to get challenge id and programming language from URL
    user_id = current_user.id

    correct_answer = Challenges.query.with_entities(Challenges.solution).filter_by(id=1).first()
    answer = request.form.get('answer')
    correct = (correct_answer == answer)
    var = Users.query.with_entities(Users.name, Users.email).join(ChallengesStats).join(Challenges).first()

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # check if user has tried the challenge already
    var = ChallengesStats.query.filter_by(challenges_id=1,users_id=user_id).first()

    if var: # if it exists, update some of the stats
        var.solved = correct
        var.end_date=ts if correct else None
        var.tries += 1
    else:
        var = ChallengesStats(challenges_id=1,  users_id=user_id, start_date=ts, end_date =ts if correct else None, tries=1, programming_languages_id=1)
        db.session.add(var)

    db.session.commit()

    return str(correct_answer == answer)

# background process happening without any refreshing
@auth.route('/background_process_test')
def background_process_test():

    user_id = current_user.id
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # we need to recover challenge and language id
    var = ChallengesStats.query.filter_by(users_id=user_id, challenges_id=2, programming_languages_id=2).first()

    if var: # if the entry exists (meaning user already started/tried the challenge before)
        if not var.start_date: # if start time was not set before, set it now
            var.start_date = ts
    else: # create the entry with the current timestamp as start_date
        var = ChallengesStats(challenges_id=2,  users_id=user_id, start_date=ts, end_date=None, programming_languages_id=2)
        db.session.add(var)

    db.session.commit()
    return "nothing"

@auth.route('/test2', methods=['POST'])
def test2():
    print("Test2")
    return "testing"
