import os
from datetime import date

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
    db_init_records()


def db_init_records():
    new_actor = (Actor(name='Johnny Deff', gender='Male', age=60))

    new_movie = (Movie(title='Pirates of Caribbean',
                 release_date=date.today()))

    new_cast = Cast.insert().values(
        Movie_id=new_movie.id, Actor_id=new_actor.id, actor_fee=500.00)

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_cast)
    db.session.commit()


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

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

# Movie


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actor', secondary=Cast, backref=db.backref(
        'casts', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
