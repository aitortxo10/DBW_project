from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from . import db
from email_validator import validate_email, EmailNotValidError
import datetime
from pylint.lint import Run

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
        flash('User not registered, please sign up')
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
    user_id=current_user.id
    id=id
    language=language
    challenge=Challenges.query.filter_by(id=id).first()
    Stats = ChallengesStats.query.filter_by(challenges_id=id,users_id=user_id).first()
    return render_template('detailed_exercise.html',challenge=challenge, id=id, language=language, Stats=Stats)

@auth.route('/detailed_exercise/<id>/<language>', methods=['POST'])
def detailed_exercise_post(id, language):
    # we have to get challenge id and programming language from URL
    user_id = current_user.id
    id=id
    language=language

    correct_answer = Challenges.query.with_entities(Challenges.solution).filter_by(id=id).first()
    answer = request.form.get('answer')
    correct = (correct_answer == answer)

    if correct == True:
        var = Users.query.with_entities(Users.name, Users.email).join(ChallengesStats).join(Challenges).first()

        time=datetime.datetime.now()
        ts = time.strftime('%Y-%m-%d %H:%M:%S')

        # check if user has tried the challenge already
        var = ChallengesStats.query.filter_by(challenges_id=id,users_id=user_id).first()

        if var: # if it exists, update some of the stats
            var.solved = correct
            var.end_date=ts
            var.tries += 1
        else:
            var = ChallengesStats(challenges_id=id,  users_id=user_id, start_date=ts, end_date =ts if correct else None, tries=1, programming_languages_id=1)

        start = datetime.datetime.strptime(var.start_date, '%Y-%m-%d %H:%M:%S')
        df=(time-start).total_seconds()
        reference=df/172800  #Two days should be the standard to solve a problem

        if reference <= 1:
            pen_time=0
        elif reference<=1.5:
            pen_time=0.5
        elif reference <=2:
            pen_time=1
        elif reference <=2.5:
            pen_time=1.5
        elif reference <= 3:
            pen_time=2
        else:
            pen_time=2.5

        if var.tries >4:
            pen_tries = 2.5
        else:
            pen_tries = 0.5*var.tries

        hints=request.form.get("hints")

        uploaded_file=request.files['files']
        if uploaded_file:
            results = Run([uploaded_file], do_exit=False)
            mark=results.linter.stats['global_note']

            if mark <=0:
                pen_pyl=2.5
            elif mark <=2:
                pen_pyl=2
            elif mark <=4:
                pen_pyl=1.5
            elif mark <=6:
                pen_pyl=1
            elif mark <=8:
                pen_pyl=0.5
            else:
                pen_pyl=0
        else:
            pen_pyl=2.5

        score=10 - 2.5*hints - pen_tries - pen_time -pen_pyl

        db.session.add(var)
        db.session.commit()

        flash("Problem solved correctly")
        return redirect(url_for('exercises'))

    else:
        flash("Incorrect Answer")
        return render_template('detailed_exercise.html',challenge=challenge, id=id, language=language)

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

