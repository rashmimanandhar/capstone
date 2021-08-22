import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import *


def create_app(test_config=None):
    setup_db(app)
    db_drop_and_create_all()

    CORS(app)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
