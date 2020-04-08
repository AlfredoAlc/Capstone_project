from flask import Flask, request, jsonify, abort, json
from flask_cors import CORS
from models import setup_db, Movies, Actors, db_drop_and_create_all
import json
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):

        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')

        return response

# ____________Movies endpoints____________

# Show all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def show_movies(token):

        try:
            data = Movies.query.all()
            movies = [Movies.format(movie) for movie in data]
            return jsonify({
               'success': True,
               'movies': movies
            })
        except Exception:
            abort(404)


# Add new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):

        try:
            body = request.get_json()
            print(body)
            new_title = body.get('title')
            print(new_title)
            new_release_date = body.get('release_date')
            print(new_release_date)

            movie = Movies(title=new_title, release_date=new_release_date)
            Movies.insert(movie)

            return jsonify({
                'success': True,
                'movie_added': Movies.format(movie)
            })

        except Exception:
            abort(422)


# Update a selected movie
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):

        try:
            movie = Movies.query.get(movie_id)
            body = request.get_json()

            if 'title' in body:
                new_title = body.get('title')
                setattr(movie, 'title', new_title)
            if 'release_date' in body:
                new_release_date = body.get('release_date')
                setattr(movie, 'release_date', new_release_date)

            Movies.update(movie)
            movie_updated = Movies.query.get(movie_id)

            return jsonify({
                'success': True,
                'movie_updated': Movies.format(movie_updated)
            })
        except Exception:
            abort(404)


# Delete selected movie
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):

        try:
            movie = Movies.query.get(movie_id)
            Movies.delete(movie)

            return jsonify({
                'success': True,
                'movie_id_deleted': movie_id
            })
        except Exception:
            abort(404)

# ____________Actors endpoints____________

# Show all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def show_actors(token):

        try:
            data = Actors.query.all()
            actors = [Actors.format(actor) for actor in data]
            return jsonify({
               'success': True,
               'actors': actors
            })
        except Exception:
            abort(404)


# Add new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):

        try:
            body = request.get_json()
            new_name = body.get('name')
            new_age = body.get('age')
            new_gender = body.get('gender')

            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            Actors.insert(actor)

            return jsonify({
                'success': True,
                'actor_added': Actors.format(actor)
            })

        except Exception:
            abort(422)


# Update a selected actor
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):

        try:
            actor = Actors.query.get(actor_id)

            body = request.get_json()

            if 'name' in body:
                new_name = body.get('name')
                setattr(actor, 'name', new_name)
            if 'age' in body:
                new_age = body.get('age')
                setattr(actor, 'age', new_age)
            if 'gender' in body:
                new_gender = body.get('gender')
                setattr(actor, 'gender', new_gender)

            Actors.update(actor)
            actor_updated = Actors.query.get(actor_id)

            return jsonify({
                'success': True,
                'actor_updated': Actors.format(actor_updated)
            })
        except Exception:
            abort(404)


# Delete selected actor
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):

        try:
            actor = Actors.query.get(actor_id)
            Actors.delete(actor)

            return jsonify({
                'success': True,
                'actor_id_deleted': actor_id
            })
        except Exception:
            abort(404)


# ____________Error handlers____________
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
                }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    return app

app = create_app()
app.run()