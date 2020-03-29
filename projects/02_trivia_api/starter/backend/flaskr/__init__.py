import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
# from flask_migrate import Migrate

# from models import setup_db, db, Question, Category
from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
 #   migrate = Migrate(app, db)

    def paginated_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [q.format() for q in selection]
        current_questions = questions[start:end]
        return current_questions

    def paginated_categories(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        categories = [c.format() for c in selection]
        current_categories = categories[start:end]
        return current_categories
    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, PUT')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        category = {c.id: c.type for c in categories}
        if category == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': category,
            'total_categories': len(Category.query.all())
        })
    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def retrieve_questions():
        questions_query = Question.query.order_by(Question.id).all()
        questions = paginated_questions(request, questions_query)

        categories_query = Category.query.order_by(Category.id).all()
        categories = {c.id: c.type for c in categories_query}

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(Question.query.all()),
            'categories': categories,
            'current_category': None,
        })
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginated_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)
    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/add', methods=['POST'])
    def new_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginated_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'tatal_questions': len(Question.query.all())
            })
        except:
            abort(422)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = Question.query.filter(
            Question.question.ilike("%" + str(body.get('searchTerm')) + "%"))
        q = paginated_questions(request, search)
        return jsonify({
            'success': True,
            'questions': q,
            'total_questions': len(q)
        })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:id>/questions')
    def questions_by_categories(id):
        results = Question.query.filter(Question.category == id)
        questions = paginated_questions(request, results)

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions)
        })
    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/play', methods=['POST'])
    def play(questions):
        body = request.get_json()
        category = body.get('categories')
        category_id = Category.query.with_entities(
            Category.id).filter(Category.type == category)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions', None)
        subset = [q for q in Question.query.order_by(
            Question.id).filter(Question.category == category.get('id')) if q.id not in previous_questions]

        if(len(subset) == 0):
            return jsonify({
                'question': None
            })

        question = random.choice(subset)
        return jsonify({
            'success': True,
            'question': Question.format(question)
        })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422


    return app
