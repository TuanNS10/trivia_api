# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.


## Documentation API

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain on which the flask server is running.

**_http://127.0.0.1:5000/_**

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

`GET '/questions?page=${int}'`

- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, all categories, and current category

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
  ],
  "success": true,
  "totalQuestions": 30
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id 
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category

```json
{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
  ],
  "success": true,
  "totalQuestions": 40
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: the appropriate HTTP status code.

---

---

`POST '/questions'`

- Sends a post request to add a new question
- Request Body:

```json
{
  "question": "New questions",
  "answer": "New answer",
  "difficulty": 4,
  "category": 3
}
```

- Returns: Question id

---

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "This is the search term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Here is a question",
      "answer": "Here is an answer",
      "difficulty": 3,
      "category": 4
    }
  ],
  "totalQuestions": 5
}
```

`POST '/quizzes'`

- Request Body:

```json
{
  "previous_questions": [10, 12, 8],
  "quiz_category": {"id": 2, "type": "Art"}
}
```

- Returns: Random questions

```json
{
  "success": true,
  "question": {
    "id": 20,
    "question": "What is the heaviest organ in the human body?",
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4
  }
}

```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

Output: (.venv) PS D:\udacity\fullstack_web_dev\trivia_API\backend> py test_flaskr.py
D:\udacity\fullstack_web_dev\trivia_API\backend\.venv\lib\site-packages\flask_cors\core.py:322: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.10 it will stop working       
  and isinstance(obj, collections.Iterable)):
D:\udacity\fullstack_web_dev\trivia_API\backend\.venv\lib\site-packages\werkzeug\local.py:206: DeprecationWarning: '__ident_func__' is deprecated and will be removed in Werkzeug 2.1. It should not be used in Python 3.7+.
  return self._local.__ident_func__
.............
----------------------------------------------------------------------
Ran 13 tests in 30.990s

OK
```
