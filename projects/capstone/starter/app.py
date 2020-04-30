#heroku run python manage.py db upgrade --directory app/migrations --app sheffercapstone
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow_Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow_Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        return "Hello" 

    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actor.query.all()
        if not actors:
            abort(400, {"message:" "Could not query actors"})
        all_results = [result.format() for result in actors]

        if len(actors) == 0:
            abort(404, {"message": "No actors currently"})
        
        
        return jsonify({"success": True, "actors": all_results}), 200

    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movie.query.all()
        if not movies:
            abort(400, {"message:" "Could not query movies"})
        all_results = [result.format() for result in movies]
        if len(movies) == 0:
            abort(404, {"message": "No movies currently"})
        return jsonify({"success": True, "movies": all_results}), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):
        data = request.get_json()
        print(request)
        if not data:
            abort(400, {"message:" "JSON body is empty"})
        name = data.get("name")
        age = data.get("age")
        gender = data.get("gender")
        new_actor = Actor(name = name, age = age, gender = gender)
        new_actor.insert()

        return jsonify({"success": True, "actor": new_actor.id}), 200

    @app.route("/movies", methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):

        data = request.get_json()
        if not data:
            abort(400, {"message:" "JSON body is empty"})
        title = data.get("title")
        release_date = data.get("release_date")

        new_movie = Movie(title = title, release_date = release_date)
        new_movie.insert()

        return jsonify({"success": True, "movie": new_movie.id}), 200

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth('patch:actors')
    def modify_actor(token):

        actor_id_place = request.url.find('/actors/') + 8

        actor_id = int(request.url[actor_id_place:])

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor : raise
            body = request.get_json()
            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)
            actor.update()
            return jsonify({"success": True, "actor_id": actor.id}), 200
        # except AuthError:
        #     abort()
        except:
            if not actor: abort(404)
            abort(422)

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    def modify_movie(token):

        movie_id_place = request.url.find('/movies/') + 8

        movie_id = int(request.url[movie_id_place:])

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if not movie : raise
            body = request.get_json()
            movie.title = body.get('title', movie.title)
            movie.release_date = body.get('release_date', movie.release_date)
            print(movie.release_date)
            movie.update()
            return jsonify({"success": True, "movie": movie.id}), 200
        #except AuthError:
        #    abort()
        except:
            if not movie: abort(404)
            abort(422)

    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(token):

        actor_id_place = request.url.find('/actors/') + 8

        actor_id = int(request.url[actor_id_place:])
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404, {"message": "This actor does not exist"})
        actor.delete()

        return jsonify({"success": True, "actor": actor.id}), 200

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(token):
        print("here")
        movie_id_place = request.url.find('/movies/') + 8

        movie_id = int(request.url[movie_id_place:])
        print("movie_id")
        print(movie_id)
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, {"message": "This movie does not exist"})
        movie.delete()

        return jsonify({"success": True, "movie": movie.id}), 200


    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(404)
    def resourceNotFound(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                "success": False,
                "error": 400,
                "message": "bad request",
                }),400

    @app.errorhandler(403)
    def no_permission(error):
        return jsonify({
                "success": False,
                "error": 403,
                "message": "no_permission",
                }),403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
                "success": False,
                "error": 401,
                "message": "unauthorized",
                }),401

    return app
app = create_app()

if __name__ == '__main__':
    #port = init(os.environ.get("PORT", 5432))
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', debug=True)
