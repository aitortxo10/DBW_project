from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

flask_key=os.urandom(16)

def create_app():
    app = Flask(__name__)

    #We need to set ut a key for the flask login function
    app.config['SECRET_KEY'] = flask_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    #Flask has a built in login manager which we will use to keep track of the user session. Before initializing the app, we need to set up how it
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) #we will use the primary key of the user table to identify the user in the session

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
