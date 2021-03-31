from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from . import db
from .models import *

main=Blueprint('main', __name__)

@main.route('/')

def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    # load user statistics
    last_login = Users.query.with_entities(Users.last_login).filter_by(id=user_id).first()[0]
    solved = ChallengesStats.query.with_entities(ChallengesStats.solved, Challenges.level).filter_by(users_id=user_id, solved=True).join(Challenges).all()
    total_solved = len(solved)
    total_score = sum(chall.level for chall in solved)
    pending = db.session.query(ChallengesStats).filter(ChallengesStats.users_id==user_id, ChallengesStats.solved!=True).all()

    total_pending = len(pending)

    challenge_data = ChallengesStats.query.filter_by(solved=True, users_id=user_id).all()

    r_solved=0
    perl_solved=0
    python_solved=0

    for item in challenge_data:
        if item.programming_languages_id==1:
            python_solved+=1
        elif item.programming_languages_id==2:
            perl_solved+=1
        else:
            r_solved+=1

    return render_template('profile.html', name=current_user.name, last_login=last_login, total_solved = total_solved,
        total_score=total_score, total_pending=total_pending,r_data=r_solved, perl_data=perl_solved, python_data=python_solved)
