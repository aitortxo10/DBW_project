from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Challenge(db.Model):
    idChallenge = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    Instructions = db.Column(db.Text(10000000))
    Test_data = db.Column(db.Text(10000000))
    Solution = db.Column(db.Text(10000000))
    Hint = db.Column(db.Text(10000000))
    Level = db.Column(db.Integer)

class Category(db.Model):
    idCategory = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))

class Programming_language(db.Model):
    idLanguage = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
