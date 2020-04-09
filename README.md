# Captsone Project: Casting Agency

This project was made to practice how to implement a backend aplication, implementing endpoints to add, delete, update and get data from a database,
all endpoints are in need of authorization from users and it has a test file in which is tested each endpoint in success and in fail state.

This is a backend project for a casting agency company, it is capable of adding movies names and release dates to a database as well as adding autors
entering the name, age and gender of each into the database. It needs a users and passwords for some endpoints.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


### Pre-requisites
Developers using this project should already have Python3 installed on their local machines.

#### Backend
In the project folder `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=app.py
flask run
```
The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

The heroku URL is https://capstone-project-agency.herokuapp.com/

### Test
To test all endpoints and authorization's tokens is a file named capstone-project.postman_collection which includes three users with differents permissions.

Role Casting Assistant:
-get:movies
-get:actors

Role Casting Director:
-get:movies
-get:actors
-post:actors
-patch:movies
-patch:actors
-delete:actors

Role Excecutive Producer:
-get:movies
-get:actors
-post:movies
-post:actors
-patch:movies
-patch:actors
-delete:movies
-delete:actors


Or it can run
```
python3 test.py
```
Will run all 14 test in the file, this file includes token for each role and test the authorization and implementation of each endpoint and fail test for each endpoint.


## Endpoints

### GET /movies

Require permission of any user.
Returns a list of movies.
```
return jsonify({
    'success': True,
    'movies': movies
     })
```

### POST /movies

Require permission of Excecutive Producer.
Create a new movie using the submited title and release_date.
Returns the movie added in a format, example:
```
"movie_added": {
    "id": 1,
    "release_date": "June 25, 1999",
    "title": "Armagedon"
}
```

### PATCH /movies/<movie_id>

Require permission of Casting Director or Excecutive Producer.
Modify the movie by the id given using title and release_date if entered.
Returns the movie modified in a format, example:
```
"movie_updated": {
    "id": 1,
    "release_date": "2001",
    "title": "Fast and Furious"
}
```

### DELETE /movies/<movie_id>

Require permission of Excecutive Producer.
Delete the movie by the id given.
Returns the id of the movie deleted.
```
return jsonify({
    'success': True,
    'movie_id_deleted': movie_id
})
```

### GET /actors

Require permission of any user.
Returns a list of actors.
```
return jsonify({
    'success': True,
    'actors': actors
     })
```

### POST /actors

Require permission of Casting Director or Excecutive Producer.
Create a new actor using the submited name, age and gender.
Returns the actor added in a format, example:
```
"actor_added": {
    "name": "Peter",
    "age": 27,
    "gender": "male"
}
```

### PATCH /actors/<actor_id>

Require permission of Casting Director or Excecutive Producer.
Modify the actor by the id given using name, age and gender if entered.
Returns the actor modified in a format, example:
```
"actor_added": {
    "name": "Jhon",
    "age": 27,
    "gender": "male"
}
```

### DELETE /actors/<actor_id>

Require permission of Casting Director or Excecutive Producer.
Delete the actor by the id given.
Returns the id of the actor deleted.
```
return jsonify({
    'success': True,
    'actor_id_deleted': actor_id
})
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resourse not found"
}

{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}
```

