# API Development and Documentation Final Project

## Trivia App
Reminder this project is carried out in a winodws environment.
To get started first install the latest python from https://www.python.org/, for this project we are working with python 3.10
Install postgresql from this https://www.postgresql.org/download/ website.
It's recommended to work in a virtual environemnt, to manage and separate your projects.
To install a virtual environment, use the following commands while in the project directory.
py -m venv venv
To activate the virtual environment utilize this command 
   venv\Scripts\activate

# Initally make sure your frontend is working well,
While in the venv environment, cd to your frontend, then utilize the following instructions to start your frontend,
 npm install
 npm start
If your frontend is unable to start, utilize this command, npm audit fix, after that try npm start again

Since we have a postgress based database, make sure you can correctly populate your database using the file trivia.psql provided in the backend folder. Make sure you are in the backend folder from there start up your postgres server.
   psql -U postgres  - To start your postgres server,
   create database trivia; -To create the trivia database
Try to populate your database using the following commands,
  psql trivia < trivia.psql
If the above command doesnt work use this one provided below.
  psql -U postgres -f trivia.psql trivia
## Next step, to install the dependencies from the requirements.txt on the backend
While in your backend folder, run the following command to install the necessary dependencies
  pip install -r requirements.txt or pip3 install -r requirements.txt

Test to see if your backend can run properly, using the following commands
  set FLASK_APP=app.py
  set FLASK_ENV=development
  flask run
we can also run our app using the command python app.py or python3 app.py depending on your python installation, because we have included the if __name__ == '__main__': at the end of our app.py file.

## Deploying testing
We have a test_flaskr.py file in our backend folder in order to run the test properly utilize the following instructions.
First open up your postress server from the same directory and run the following commands to populate the  test database
   -dropdb trivia_test
   -createdb trivia_test
   -psql trivia_test < trivia.psql or psql -U postgres -f trivia.psql trivia_test
After successful population of our test database, utilize the following command to run our python file
   -python3 test_flaskr.py or python test_flaskr.py   
##The current base URL for the backend app is http://127.0.0.1:5000/  , while the fronend is hosted in this local address http://localhost:3000/,

## API End points
Reminder for curl requests utilized thunder client addon to test each endpoints.
# GET '/categories' (http://127.0.0.1:5000/categories)
Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs, plus a success message.
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
# GET '/questions?page=${integer}' (http://127.0.0.1:5000/questions?page=${integer})

Fetches a paginated set of questions, a total number of questions, all categories and current category string.
Request Arguments: page - integer
Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },

# GET 'categories/${integer}/questions' (http://127.0.0.1:5000/categories/${integer}/questions) 

Fetches questions for a cateogry specified by id request argument
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string
{
  "current_catogory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
  "success": true,
  "total_questions": 100
}
## DELETE '/questions/${id}'
Deletes a specified question using the id of the question
Request Arguments: id - integer
Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
## POST '/quizzes'
Sends a post request in order to get the next question
Request Body:
{
    'previous_questions': [1, 4, 20, 15]    ## quiz_category{"id":0, "type":"All"}}
    quiz_category': 'current category'
}
Returns: a single new question object
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
## POST '/questions' (http://127.0.0.1:5000/questions)
Sends a post request in order to add a new question
Request Body:
{
    'question':  'Who won the ballon d'or 2018?',
    'answer':  'Luke Modric',
    'difficulty': 3,
    'category': 6
}
Returns: Does not return any new data

## POST '/questions' (http://127.0.0.1:5000/questions) this is for the search function
Sends a post request in order to search for a specific question by search term
Request Body:
{"searchTerm":"Tom"}
Returns:any array of questions, a number of totalQuestions that met the search term and the current category string plus a success messge.
{
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 100
}
