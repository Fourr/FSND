# Capstone Project of FSND: Casting Agency

## Motivation
My motivation for this project was to apply all the skills learned during this Full stack Nanodegree program.
Following topics, libraries and skills learnt as part of this program:
1. SQL and database modeling for the web ```(SQL, flask-sqlalchemy, flask-migrate)```
2. API development and documentation ```(flask, unittest)```
3. Identity and access management ```(Auth0)```
4. Server deployment and Containerization ```(docker and kubernetes)```


This app has been deployed on heroku:
[URL of this app](https://sheffercapstone.herokuapp.com/actors)


## Project dependencies, local development and hosting instructions

1. First cd into the project folder
2. Install [python](https://www.python.org/downloads/) and [postgres](https://www.postgresql.org/download/).

3. Install the dependencies:
```
pip3 install requirements.txt
```
4. Setup database in ```models.py ```:
```
database_path = "postgres://{}:{}@{}/{}".format(<user-name>,'<password>','localhost:5432', <database_name>)
```

5. Setup Auth0:
 - create an account on auth0
 - Create an application  <casting-agency>
 - Create an API <castings>
 - Define permissions in API. Following permissions defined :
 ``` 
 get:actors, get:movies, post:actor, post:movie, patch:actor, patch:movie, delete:actor, delete:movie
 ```
 - Define role: Casting Director and Casting Producer 
 - Give permissions to the roles

6. ```export FLASK_APP=app.py export FLASK_ENV=development```
7. Now start local development server
```flask run ```

8. All endpoints written in ```app.py```, models in ```models.py```, config variable in ```config.py``` and all dependencies are in ```requirements.txt```
9. To tun the ```test_app.py``` file, execute ```python3 test_app.py```.

## API documentation and RBAC controls

The roles and their permissions have been explained here:

1. Casting director has the following permissions:
- GET /actors: Can view all actors
- GET /movies: Can view all movies
- PATCH /actors/<actor-id>: Can modify an actor
- PATCH /movies/<movies-id>:Can modify a movie
- DELETE /actors/<actor-id>: Can delete an actor
- POST /actors: Can add a new actor

2. Casting producer has the same permissions as a casting director with the additional:
- POST /movies: Can a add movie
- DELETE /movies/<movie-id>: Can delete a movie

All the endpoints and routes of this app have been explained here:

### GET /actors
- Returns a list of all actors and their details :name,age and gender.
- Send the following request with ```Authorization header``` (It contains ```get:actors``` permission)

 ```
 https://sheffercapstone.herokuapp.com/actors
 ```
- Gives following response:
```
{
  "actors": [
    {
      "age": 45,
      "gender": "Male",
      "id": 1,
      "name": "Leonardo DiCaprio"
    }
  ],
  "success": true
}
```
- If request is sent without required permission ```delete:actors```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}

### GET /movies
- Returns a list of all movies and details : title and release_date.
- Send the following request with ```Authorization header``` (It contains ```get:movies``` permission)

- Casting assistant, casting director and casting producer have the permission to get movies.
 ```
 https://sheffercapstone.herokuapp.com/movies
 ```
- Gives following response:
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "08-06-2012",
      "title": "The Other Guys"
    }
  ],
  "success": true
}
```
- If request is sent without required permission ```get:movies```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}
### POST /actors
- Add a new actor in the database and return success and the id of newly created record.
- Send following json in the body:
```
{
    "name": "Leonardo DiCaprio",
    "age": "45",
    "gender": "Male"
}
```
- Must have a token which has ```add:actor``` permission. 
- Send a POST request to this url:
```
https://sheffercapstone.herokuapp.com/actors
```
- It gives this response:
```
{
    "actor": 1,
    "success": true
}
```
- If request is sent without required permissions , gives this response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}
```

### POST /movies
- Add a new movie in the database and return success and the id of newly created record.
- Send following json in the body:
```
{
    "title": "The Other Guys",
    "release_date": "08-06-2010"
}

```
- Also send the token which has ```add:movie``` permission. Only Casting producer have the permission to do so.
- Send a POST request to this url:
```
https://sheffercapstone.herokuapp.com/movies
```
- It gives this response:
```
{
  "movie": 1,
  "success": true
}
```
- If request is sent without required permissions , gives this response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}
```
### Patch /actors/<int:actor_id>
- Updates an actor with given id and return success message with id of modified actor.
- Authorization header must have ``` modify:actor ``` permission.
- Send patch request to:
```
https://sheffercapstone.herokuapp.com/actors/3
```
- Send request with a json body:
```
{
    "gender": "Female"
}
```
- Return following response:
```
{
  "actor_id": 5,
  "success": true
}
```
- If request is sent without required permission ```modify:actor```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}
```

### Patch /movies/<int:movie_id>
- Updates a movie with given id and return success message with id of modified movie.
- Authorization header must have ``` modify:movie ``` permission.
- Send patch request to:
```
https://sheffercapstone.herokuapp.com/movies/1
```
- With JSON body:
```
{
    "release_date": "08-06-2012"
}
```
- Return this reponse
```
{
  "movie": 1,
  "success": true
}
```
- If request is sent without required permission ```modify:actor```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}
```

### DELETE /actors/<actor_id>
- Deletes the given actor record and return success message with the of deleted actor.
- Authorization header should have ``` delete:actor ``` permission.
- Send DELETE request to this url:
```
https://sheffercapstone.herokuapp.com/actors/1
```
- Returns this response:
```
{
  "actor": 1,
  "success": true
}
```
- If request is sent without required permission ```delete:actors```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}

### DELETE /movies/<movie_id>
- Deletes the given movie record and return success message with the of deleted movie.
- Authorization header should have ``` delete:movie ``` permission.
- Send DELETE request to this url:
```
https://sheffercapstone.herokuapp.com/movies/1
```
- Returns this response:
```
{
  "movie": 1,
  "success": true
}
```
- If request is sent without required permission ```delete:movies```
- Gives following response:
```
{
  "error": 403,
  "message": "no_permission",
  "success": false
}