from flask_login import UserMixin
from . import db
from sqlalchemy.orm import relationship

# Many-to-Many relationships needs to a helper table (established wtih db.Table)

categories_challenges = db.Table('categories_challenges',
                                db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
                                db.Column('challenges_id', db.Integer, db.ForeignKey('challenges.id'), primary_key=True))

languages_challenges = db.Table('languages_challenges',
                                db.Column('challenges_id', db.Integer, db.ForeignKey('challenges.id'), primary_key=True),
                                db.Column('programming_languages_id', db.Integer, db.ForeignKey('programming_languages.id'), primary_key=True),
                                db.Column('example_code', db.Text))

challenges_stats = db.Table('challenges_stats',
                            db.Column('challenges_id', db.Integer, db.ForeignKey('challenges.id'), primary_key=True),
                            db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                            db.Column('start_date', db.DateTime),
                            db.Column('end_date', db.DateTime),
                            db.Column('tries', db.Integer),
                            db.Column('solved', db.Boolean),
                            db.Column('programming_languages_id', db.Integer, db.ForeignKey('programming_languages.id')))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(1000))
    age = db.Column(db.Integer)
    country = db.Column(db.String(45))
    background = db.Column(db.String(45))

    # many-to-many Users <-> Challenges
    challenges = relationship('Challenges', secondary=challenges_stats, back_populates='users')

class Challenges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    instructions = db.Column(db.Text)
    test_data = db.Column(db.Text)
    solution = db.Column(db.Text)
    hint = db.Column(db.Text)
    level = db.Column(db.Integer)

    # many-to-many Users <-> Challenges
    users = relationship('Users', secondary=challenges_stats, back_populates='challenges')

    # many-to-many Languages <-> Challenges
    languages = relationship('ProgrammingLanguages', secondary=languages_challenges, back_populates='challenges')

    #languages = db.relationship('ProgrammingLanguages', secondary = languages_challenges, backref=db.backref('ProgrammingLanguages', lazy='dynamic'))

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

class ProgrammingLanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

    # many-to-many Languages <-> Challenges
    challenges = relationship('Challenges', secondary=languages_challenges, back_populates='languages')
