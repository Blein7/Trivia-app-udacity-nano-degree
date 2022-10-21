import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category

#When running the delete tests,remember to change the id inorder to run the tests successfully again 
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "admin","localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question ={'question': 'question','answer': 'answer','difficulty': 1,'category': 1}
        self.new_quiz={'previous_questions': [10,12],'quiz_category': {'type': 'Art', 'id': 2}}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue((data["categories"]))
        #self.assertTrue(data["current_category"])
        

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")
        
    def test_z_delete_question(self):
        res = self.client().delete("/questions/13")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 13)
        self.assertEqual(question, None)

    def test_Z_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        
    def test_get_specific_questions(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)
        
        categories = Category.query.filter(Category.id ==2).one_or_none()
        questions  = Question.query.filter(Question.category==categories.id).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"],questions)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["current_catogory"],categories.type)

    def test_422__if_category_does_not_exist(self):
        res = self.client().get("/categories/7/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")    
    
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_if_question_creation_not_allowed(self):
        self.new_question ={'question': 'question','answer': '','difficulty': 1,'category': 1}
        res = self.client().post("/questions/800", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")   
    
    def test_quiz(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_quiz_error(self):
        self.new_quiz= {'previous_questions': []}
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")     
    
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "Tom"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 1)


    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "Football"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"],[])
        self.assertEqual(len(data["questions"]), 0)  

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()