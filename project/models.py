from flask_login import UserMixin
from . import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

# Many-to-Many relationships needs to a helper table (established wtih db.Table)

categories_challenges = db.Table('categories_challenges',
                                db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
                                db.Column('challenges_id', db.Integer, db.ForeignKey('challenges.id'), primary_key=True))

# challenges_stats = db.Table('challenges_stats',
#                             db.Column('challenges_id', db.Integer, db.ForeignKey('challenges.id'), primary_key=True),
#                             db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#                             db.Column('start_date', db.DateTime),
#                             db.Column('end_date', db.DateTime),
#                             db.Column('tries', db.Integer),
#                             db.Column('solved', db.Boolean),
#                             db.Column('programming_languages_id', db.Integer, db.ForeignKey('programming_languages.id')))

class LanguagesChallenges(db.Model):
    __tablename__ = 'languages_challenges' # useless but added it anyway

    challenges_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), primary_key=True)
    programming_languages_id = db.Column(db.Integer, db.ForeignKey('programming_languages.id'), primary_key=True)
    example_code = db.Column(db.Text)

    # establishing one-to-many relationship ProgrammingLanguages <-> Challenges
    challenges = relationship("Challenges", back_populates= "languages") # backpopulates refers to the attribute languages of the class Challenges
    languages = relationship("ProgrammingLanguages", back_populates= "challenges")

class ChallengesStats(db.Model):
    __tablename__ = 'challenges_stats'

    challenges_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    tries = db.Column(db.Integer)
    solved = db.Column(db.Boolean)
    programming_languages_id = db.Column(db.Integer, db.ForeignKey('programming_languages.id'))

    # establishing many-to-many relationship Users <-> Challenges
    challenges = relationship("Challenges", back_populates="users")
    users = relationship("Users", back_populates="challenges")

    def __repr__(self): # objects are represented as Stats(0001) for instances belonging to user 0001
        return "Stats(%s)" %repr(self.users_id)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(1000))
    last_login = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    country = db.Column(db.String(45))
    background = db.Column(db.String(45))

    # one-to-many ChallengesStats <-> Users
    challenges = relationship('ChallengesStats', back_populates='users')

class Challenges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    instructions = db.Column(db.Text)
    test_data = db.Column(db.Text)
    solution = db.Column(db.Text)
    hint = db.Column(db.Text)
    level = db.Column(db.Integer)

    # one-to-many ChallengesStats <-> Challenges
    users = relationship('ChallengesStats', back_populates='challenges')

    # one-to-many LanguagesChallenges <-> Challenges
    languages = relationship("LanguagesChallenges", back_populates="challenges")

    def __repr__(self):
        return "Challenge(%s)" %repr(self.name)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

class ProgrammingLanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

    # one-to-many Languages <-> LanguagesChallenges
    challenges = relationship("LanguagesChallenges", back_populates = "languages")
