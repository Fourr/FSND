import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from auth import AuthError, requires_auth
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
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting
    @app.route('/actors', methods=["GET"])
    #@requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.all()
        if not actors:
            abort(400, {"message:" "Could not query actors"})
        all_results = [result.format() for result in actors]

        if len(actors) == 0:
            abort(404, {"message": "No actors currently"})
        
        
        return jsonify({"success": True, "actors": all_results}), 200

    @app.route('/movies', methods=["GET"])
    def get_movies():
        movies = Movie.query.all()
        if not movies:
            abort(400, {"message:" "Could not query movies"})
        all_results = [result.format() for result in movies]
        if len(movies) == 0:
            abort(404, {"message": "No movies currently"})
        return jsonify({"success": True, "movies": all_results}), 200

    @app.route('/actors', methods=['POST'])
    def add_actor():
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
    def add_movie():

        data = request.get_json()
        if not data:
            abort(400, {"message:" "JSON body is empty"})
        title = data.get("title")
        release_date = data.get("release_date")

        new_movie = Movie(title = title, release_date = release_date)
        new_movie.insert()

        return jsonify({"success": True, "movie": new_movie.id}), 200

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    #@requires_auth("modify:actor")
    def modify_actor(actor_id):


        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor : raise
            body = request.get_json()
            actor.name = body.get('name', actor.name)
            actor.age = body.get('age', actor.age)
            actor.gender = body.get('gender', actor.gender)
            actor.update()
            return jsonify({"success": True, "actor_id": actor.id}), 200
        #except AuthError:
        #    abort()
        except:
            if not actor: abort(404)
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    #@requires_auth("modify:movie")
    def modify_movie(movie_id):

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

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    #@requires_auth("delete:actor")
    def delete_actor(actor_id):

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404, {"message": "This actor does not exist"})
        actor.delete()

        return jsonify({"success": True, "actor": actor.id}), 200

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    #@requires_auth("delete:movie")
    def delete_movie(movie_id):

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, {"message": "This movie does not exist"})
        movie.delete()

        return jsonify({"success": True, "movie": movie.id}), 200


    return app

app = create_app()

if __name__ == '__main__':
    #port = init(os.environ.get("PORT", 5432))
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', debug=True)
