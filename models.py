import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
