from dotenv import load_dotenv
import os
import requests
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app

load_dotenv()
database_path = os.getenv("DATABASE_TEST_URL")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = database_path
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        self.base_url = 'http://localhost:5000'

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        # Send GET request to /categories
        response = requests.get(f'{self.base_url}/categories')
        data = response.json()
        
        # Check status code based on whether there are categories or not
        if len(data['categories']) > 0:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
        else:
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data['success'])
        
        # Check response data
        self.assertTrue('categories' in data)
        if len(data['categories']) > 0:
            self.assertTrue(len(data['categories']) > 0)
        else:
            self.assertTrue('categories' not in data)
    
    def test_get_questions(self):
        """Test GET request to fetch questions"""
        response = requests.get(f'{self.base_url}/questions')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('current_category' in data)
        self.assertTrue('categories' in data)
    
    def test_add_question(self):
        """Test POST request to add a new question"""
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 1
        }
        response = requests.post(f'{self.base_url}/questions', json=new_question)
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('created' in data)
        self.assertTrue('total_questions' in data)
    
    def test_delete_question_success(self):
        """Test DELETE request to delete a question"""
        # Create a question to delete
        response = requests.post(f'{self.base_url}/questions', json={
            'question': 'Test Question',
            'answer': 'Test Answer',
            'category': 1,
            'difficulty': 1
        })
        data = response.json()
        question_id = data['created']

        # Send DELETE request to /questions/{question_id}
        response = requests.delete(f'{self.base_url}/questions/{question_id}')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue('total_questions' in data)

    def test_delete_question_not_found(self):
        """Test DELETE request to delete a non-existing question"""
        # Send DELETE request to /questions/{non_existing_id}
        response = requests.delete(f'{self.base_url}/questions/1000')
        data = response.json()
        
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_question_error(self):
        """Test DELETE request to delete a question with error"""
        # Send DELETE request to /questions/{invalid_id}
        response = requests.delete(f'{self.base_url}/questions/invalid_id')
        data = response.json()
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_search_questions_success(self):
        """Test POST request to search questions"""
        # Send POST request to /questions/search
        response = requests.post(f'{self.base_url}/questions/search', json={'searchTerm': 'title'})
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertEqual(data['current_category'], None)

    def test_search_questions_no_results(self):
        """Test POST request to search questions with no results"""
        # Send POST request to /questions/search
        response = requests.post(f'{self.base_url}/questions/search', json={'searchTerm': 'non_existing_term'})
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)

    def test_search_questions_error(self):
        """Test POST request to search questions with error"""
        # Send POST request to /questions/search without searchTerm
        response = requests.post(f'{self.base_url}/questions/search')
        
        self.assertEqual(response.status_code, 500)

    def test_category_questions_success(self):
        """Test GET request to fetch questions by category"""
        # Send GET request to /categories/{category_id}/questions
        response = requests.get(f'{self.base_url}/categories/1/questions')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('current_category' in data)

    def test_category_questions_category_not_found(self):
        """Test GET request to fetch questions by non-existing category"""
        # Send GET request to /categories/{non_existing_category_id}/questions
        response = requests.get(f'{self.base_url}/categories/1000/questions')
        
        self.assertEqual(response.status_code, 404)

    def test_play_quiz_success(self):
        """Test POST request to play quiz"""
        # Send POST request to /quizzes with previous_questions and quiz_category
        response = requests.post(f'{self.base_url}/quizzes', json={"previous_questions": [1, 2, 3], "quiz_category": {"id": 1, "type": "Science"}})
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('question' in data)

    def test_play_quiz_no_previous_questions(self):
        """Test POST request to play quiz with no previous questions"""
        # Send POST request to /quizzes with quiz_category only
        response = requests.post(f'{self.base_url}/quizzes', json={"quiz_category": {"id": 1, "type": "Science"}})
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('question' in data)

    def test_play_quiz_no_body(self):
        """Test POST request to play quiz with no request body"""
        # Send POST request to /quizzes without request body
        response = requests.post(f'{self.base_url}/quizzes')
        
        self.assertEqual(response.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()