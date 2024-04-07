
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random


from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [quest.format() for quest in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
    # http://127.0.0.1:5000/categories

        categories = db.session.query(Category).order_by(Category.id).all()
    
        if len(categories) == 0:
            abort(404)

        return jsonify ({
            'success': True,
            'categories': {item.id: item.type for item in categories}
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
    # http://127.0.0.1:5000/questions?page=2

        questions = Question.query.order_by(Question.id).all()

        questions_paginated = paginate_questions(request, questions)

        if len(questions_paginated) == 0:
            abort(404)

        categories = Category.query.all()

        categories_returned = [category.format() for category in categories]

        # Get the current category (defaulting to first category)
        current_category = categories_returned[0]['type'] if len(categories_returned) > 0 else None

        return jsonify({
            'success': True,
            'questions': questions_paginated,
            'total_questions': len(questions),
            'categories': [category['type'] for category in categories_returned],
            'current_category': current_category
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            
            if question is None:
                abort(404)
            
            question.delete()

            tot_question = len(Question.query.all())

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': tot_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if not (new_question and new_answer and new_category and new_difficulty):
            abort(422)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )

            question.insert()
            total_questions = Question.query.all()

            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(total_questions)
            })
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json().get('searchTerm', '')

        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            paginated_questions = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "questions": paginated_questions,
                "total_questions": len(questions),
                "current_category": None
            })
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def category_questions(category_id):
        try:
            category = Category.query.get(category_id)
            if not category:
                abort(404)

            selection = Question.query.filter_by(category=str(category_id)).all()

            if not selection:
                return jsonify({
                    "success": True,
                    "message": "No questions found for this category",
                    "current_category": category.type
                })

            paginated_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": paginated_questions,
                "total_questions": len(selection),
                "current_category": category.type
            })
        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def start_trivia():
        body = request.get_json()

        if not body:
            abort(400, {'message': 'Please provide a JSON body with previous question Ids and optional category.'})
            
        previous_questions = body.get('previous_questions', None)
        current_category = body.get('quiz_category', None)

        if not previous_questions:
            if current_category:
                # if no list with previous questions is given, but a category , just gut any question from this category.
                questions_raw = (Question.query
                .filter(Question.category == str(current_category['id']))
                .all())
            else:
                # if no list with previous questions is given and also no category , just gut any question.
                questions_raw = (Question.query.all())    
        else:
            if current_category:
                # if a list with previous questions is given and also a category, query for questions which are not contained in previous question and are in given category
                questions_raw = (Question.query
                .filter(Question.category == str(current_category['id']))
                .filter(Question.id.notin_(previous_questions))
                .all())
            else:
                # if a list with previous questions is given but no category, query for questions which are not contained in previous question.
                questions_raw = (Question.query
                .filter(Question.id.notin_(previous_questions))
                .all())
        
        questions_formatted = [question.format() for question in questions_raw]
        random_question = questions_formatted[random.randint(0, len(questions_formatted))]
        
        return jsonify({
            'success': True,
            'question': random_question
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return( 
            jsonify({'success': False, 'error': 404,'message': 'resource not found'}),
            404
        )
    
    @app.errorhandler(422)
    def unprocessed(error):
        return(
            jsonify({'success': False, 'error': 422,'message': 'request cannot be processed'}),
            422
        )


    return app

