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

    return render_template('profile.html', name=current_user.name, last_login=last_login)
