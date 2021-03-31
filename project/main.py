from flask import Blueprint, render_template
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
    pending = ChallengesStats.query.filter_by(users_id=user_id, solved=False).all()

    total_pending = []
    # obtain the language name of the pending challenges in a tuple
    for pen in pending:
        lang_name = ProgrammingLanguages.query.with_entities(ProgrammingLanguages.name).filter_by(id=pen.programming_languages_id).first()[0]
        total_pending.append((pen, lang_name))

    pending_chall = pending[0]

    return render_template('profile.html', name=current_user.name, last_login=last_login, total_solved = total_solved, total_score=total_score, total_pending=total_pending)
