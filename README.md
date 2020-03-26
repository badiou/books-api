Full Stack Trivia API Backend
Getting Started
Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

psql trivia < books.psql
Running the server


To run the server, execute:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to flaskr directs flask to use the flaskr directory and the __init__.py file to find the application.

API REFERENCE
Getting starter

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:5000; which is set as a proxy in frontend configuration.

Error Handling
Errors are retourned as JSON objects in the following format: { "success":False "error": 400 "message":"Bad request }

The API will return four error types when requests fail: . 400: Bad request . 500: Internal server error . 422: Unprocessable . 404: Not found

Endpoints
. ## GET/books

GENERAL:
    This endpoints returns a list of book object, success value, total number of the books. 

    
SAMPLE: curl http://localhost:5000/books

    {
    "books": 
        {
            
        },
    "success": true
    }

. ## DELETE /books(book_id)

GENERAL:
    Delete the book of the given ID if it exists. Return the id of the deleted book, success value, total of book and book list based on current page number to update the frontend

    Results are paginated in groups of 10. include a request argument to choose page number, starting from 1.

    SAMPLE: curl -X DELETE http://localhost:5000/books/2?page=2

     "deleted": 14,
"books": [ { }]

. ## POST/books

GENERAL:    
This endpoint is used to create a new books 

SAMPLE.....For Search:
curl -X POST http://localhost:5000/books -H "Content-Type:application/json" -d "{"title":"title"}"

            {
    "books": [
        {
        
        },
        {
        
        }
    ],
    "success": true,
    "total_books": 10
    }

SAMPLE.....For create

