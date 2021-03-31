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
        flash('User not registered, please sign up')
        return redirect(url_for('auth.login'))

    elif not check_password_hash(user.password,password): #If the password or the email is not correct, flash an error message and redirectonce more to the login page
        flash('Incorrect password, please try again')
        return redirect(url_for('auth.login'))


    login_user(user, remember=remember)
    if user.last_login:
        flash(user.last_login)
    user.last_login = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
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
    exercise_list = Challenges.query.join(LanguagesChallenges).join(ProgrammingLanguages).order_by(Challenges.level)

    if current_user.is_authenticated:
        stats=ChallengesStats.query.filter_by(users_id=current_user.id).order_by(ChallengesStats.challenges_id).all()

        id=""
        score_list=[]
        max_scores=[]

        for stat in stats:
            if not id:
                id=stat.challenges_id
                if stat.score:
                    score_list.append(int(stat.score))
                else:
                    score_list.append(-1)       #Default value for the NA due to not being solved
            else:
                if not id == stat.challenges_id:
                    max_scores.append(max(score_list))
                    score_list=[]
                else:
                    if stat.score:
                        score_list.append(int(stat.score))
                    else:
                        score_list.append(-1)
        if score_list:
            max_scores.append(max(score_list))

        return render_template('exercises.html', exercise_list=exercise_list, max_scores=max_scores)

    else:
        return render_template('exercises.html', exercise_list=exercise_list)

@auth.route('/detailed_exercise/<id>/<language>')
@login_required
def detailed_exercise(id, language):
    # get parametres from url
    id=id
    language_id=ProgrammingLanguages.query.with_entities(ProgrammingLanguages.id).filter_by(name=language).first()[0]
    challenge=Challenges.query.filter_by(id=id).first()
    user_id = current_user.id

    # check if the exercise was started before by the same user
    stats = ChallengesStats.query.filter_by(challenges_id=id,users_id=user_id, programming_languages_id=language_id).first()

    return render_template('detailed_exercise.html',challenge=challenge, id=id, language=language, stats=stats)

@auth.route('/detailed_exercise/<id>/<language>', methods=['POST'])
def detailed_exercise_post(id,language):

    # obtain parametres such as current user and challenge and language
    user_id = current_user.id
    challenge_id=int(id)
    language=language

    language_id = ProgrammingLanguages.query.with_entities(ProgrammingLanguages.id).filter_by(name=language).first()[0]
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if user answer is right
    correct_answer = Challenges.query.with_entities(Challenges.solution).filter_by(id=challenge_id).first()[0]
    user_answer = request.form.get('answer')

    correct = (str(correct_answer) == str(user_answer))

    var = ChallengesStats.query.filter_by(challenges_id=challenge_id, programming_languages_id=language_id, users_id=user_id).first()

    if not var: # if the challenge was not started
        var = ChallengesStats(challenges_id=challenge_id,  users_id=user_id, start_date=ts, tries=0, programming_languages_id=language_id, solved=False)
        db.add(var)

    var.tries+=1

    if correct == True:

        time=datetime.datetime.now()
        ts = time.strftime('%Y-%m-%d %H:%M:%S')

        if var: # if it exists, update some of the stats
            var.solved = correct
            var.end_date=ts

        #start = datetime.datetime.strptime(var.start_date, '%Y-%m-%d %H:%M:%S')
        start=var.start_date
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

        hints=int(request.form.get("hints"))

        if language == "Python3.8":

            uploaded_file=request.files['file']
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

            var.score=10 - 2.5*hints - pen_tries - pen_time -pen_pyl

        else:
            var.score=((7.5 - 2.5*hints - pen_tries - pen_time)/7.5)*10

        db.session.commit()
        flash("Problem solved correctly")
        return redirect(url_for('auth.exercises'))

    else:
        db.session.commit()
        flash("Incorrect Answer, please try again.")
        challenge=Challenges.query.filter_by(id=challenge_id).first()

        # check if the exercise was started before by the same user
        stats = ChallengesStats.query.filter_by(challenges_id=id,users_id=user_id, programming_languages_id=language_id).first()
        return render_template('detailed_exercise.html',challenge=challenge, id=id, language=language, stats=stats)

# background process happening without any refreshing
@auth.route('/create_entry/<challenge>/<language>', methods=['GET'])
def background_process_test(challenge, language):

    #obtain current user id, a current time and programming language used
    user_id = current_user.id
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    language_id = ProgrammingLanguages.query.with_entities(ProgrammingLanguages.id).filter_by(name=language).first()[0]
    challenge=int(challenge)

    # check if the entry existed already
    var = ChallengesStats.query.filter_by(users_id=user_id, challenges_id=challenge, programming_languages_id=language_id).first()

    if var: # if the entry exists (meaning user already started/tried the challenge before)
        var.start_date=ts
    else: # create the entry with the current timestamp as start_date
        var = ChallengesStats(challenges_id=challenge,  users_id=user_id, start_date=ts, programming_languages_id=language_id, tries=0, solved=False)
        db.session.add(var)


    db.session.commit()
    return "nothing"
