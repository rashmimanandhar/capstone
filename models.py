import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Float, Integer, String, create_engine

from config import DATABASE_TRACK_MODIFICATIONS, DATABASE_URL

database_path = os.environ.get('DATABASE_URL', DATABASE_URL)
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# Cast
Cast = db.Table('Cast', db.Model.metadata,
                db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
                db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
                db.Column('actor_fee', db.Float))

# Actor


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

# Movie


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actor', secondary=Cast, backref=db.backref(
        'casts', lazy='joined'))
