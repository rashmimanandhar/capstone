import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import *

ROWS_PER_PAGE = 10


def create_app(test_config=None):
    setup_db(app)
    db_drop_and_create_all()

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def paginate_results(request, selection):
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        objects = [object.format for object in selection]
        return objects[start:end]

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()
        actors_paginated = paginate_results(request, actors)

        if len(actors_paginated) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors_paginated
        })

    @app.route('/actors', methods=['POST'])
    def insert_actors():
        body = request.get_json()

        if not body:
            abort(400)
        name = body.get('name', None)
        age = body.get('age', None)

        gender = body.get('gender', 'Other')

        if not name or not age:
            abort(422)

        new_actor = (Actor(name=name, age=age, gender=gender))
        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    def edit_actors(actor_id):
        body = request.get_json()

        if not actor_id or not body:
            abort(400)

        actor_to_update = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if not actor_to_update:
            abort(404)

        name = body.get('name', actor_to_update.name)
        age = body.get('age', actor_to_update.age)
        gender = body.get('gender', actor_to_update.gender)

        actor_to_update.name = name
        actor_to_update.age = age
        actor_to_update.gender = gender

        actor_to_update.update()

        return jsonify({
            'success': True,
            'updated': actor_to_update.id,
            'actor': [actor_to_update.format]
        })

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    def delete_actors(actor_id):
        if not actor_id:
            abort(400)

        actor_to_delete = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if not actor_to_delete:
            abort(404)

        actor_to_delete.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
