import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from collections.abc import Mapping
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
   
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    #need to have a dictionary inorder to attain the id to type display of the categories, specified from the front end error
    @app.route("/categories")
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        pair_categories={category.id: category.type for category in categories}
        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": pair_categories
            }
        )

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        #need to have a dictionary inorder to attain the id to type display of the categories, specified from the front end error
        pair_categories={category.id: category.type for category in categories}
        current_value= [current.get('category', None) for current in current_questions]
        current_category=''
        for i in current_value:
            if i in pair_categories.keys():
                current_category=pair_categories[i]           
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": pair_categories,
                "current_category":current_category
            }
        )
        
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )

        except:
            abort(422)
    #Both the search and create options are within the same endpoint
    #Unable to attaint the current category for each question, at the moment just passing None value
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
                current_questions = [question.format()for question in questions]
                current_value= [current.get('category', None) for current in current_questions]
                current_category=''
                categories = Category.query.all()
                pair_categories={category.id: category.type for category in categories}
                for i in current_value:
                    if i in pair_categories.keys():
                        current_category=pair_categories[i] 
                #current category displaying last questions ctegory type, still need to display for each question        
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category":current_category
                })

            else:
                question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    "success": True
                })
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def specific_questions(category_id):
        try:
            categories = Category.query.filter(Category.id == category_id).one_or_none()
            #utilize categories.type to fetch current category
            if categories is None:
                abort(404)
            selection = Question.query.filter(Question.category==categories.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_catogory":categories.type
                }
            )

        except:
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def create_quiz():
        
        body = request.get_json()
        try:
            
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            
            if (previous_questions is None) or (quiz_category is None):
                abort(404)   
            #The id set for 'ALL' is 0, when the category is All  
            if int(quiz_category['id']==0):
                questions=Question.query.all()
                available_ids=[question.id for question in questions]
                random_num=random.choice([num for num in available_ids if num not in previous_questions])
                #runs perfectly for this part
                random_question=Question.query.filter(Question.id==random_num).one_or_none()
            else:
                questions = Question.query.filter(Question.category == quiz_category['id'],Question.id.notin_(previous_questions)).all()    
                #print(len(questions))
                if len(questions)==0:
                      return jsonify({"forceEnd": True})
                      # We can utilize the forceEnd variable on the Quizview.js to call the renderplay() function
                  
                else:
                    random_question=random.choice(questions)
                    
                
            return jsonify({
                "success": True,
                "question":random_question.format()
            })    
        except:
            abort(422)            
    #Error handlers, for curl tests utilized Thunder client vscode extention
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"Not found"
        }),404
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message":"Bad Request"
        }),400
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"Unprocessable"
        }),422
    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"Method not allowed"
        }),405       
    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":500,
            "message":"Internal server error"
        }),500     

    return app
#In order to run our app as python __init__.py
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)