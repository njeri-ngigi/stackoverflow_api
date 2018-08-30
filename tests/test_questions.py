import unittest
import json
import ast
from app import createApp

class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.app = createApp(config_name="testing")
        self.client = self.app.test_client

        #register 2 users 
        self.client().post('/api/v1/auth/signup', content_type="application/json", 
                            data=json.dumps({"name": "Njeri", "username": "njery", 
                            "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup', content_type="application/json", 
                            data=json.dumps({"name": "Suite", "username": "suite", 
                            "email": "suite@to.com", "password": "Test123", "confirm_password": "Test123"}))        
        #login in both users
        res = self.client().post('/api/v1/auth/login', content_type="application/json", 
                            data=json.dumps({"username": "njery", "password": "Test123"}))
        u_data = ast.literal_eval(res.data)
        a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json", 
                            data=json.dumps({"username": "suite", "password": "Test123"}))
        u_data2 = ast.literal_eval(res2.data)
        a_token2 = u_data2["token"]
        #post 3 questions
        self.client().post('/api/v1/questions', headers=dict(Authorization="Bearer " + a_token), content_type="application/json", data=json.dumps({"title": "Git branching", "content": "How to create and checkout a branch in git"}))
        self.client().post('/api/v1/questions', headers=dict(Authorization="Bearer " + a_token2), content_type="application/json", data=json.dumps({"title": "How to make a github page?", "content": "How do you host web templates on github using github pages"}))


    def test_questions(self):
        '''test handling posting questions'''


    def test_get_questions(self):
        '''test getting all questions and single questions'''
        #get all questions
        result = self.client().get('/api/v1/questions')
        my_data = ast.literal_eval(result.data)
        self.assertGreater(len(my_data), 0)
        self.assertEqual(result.status_code, 200)

        #get single question
        # result2 = self.client().get('/api/v1/questions/0')
        # my_data2 = ast.literal_eval(result2)
        # self.assertIn("Git branching", my_data2)
        # self.assertEqual(result2.status_code, 200)

    def test_delete_questions(self):
        '''test deleting questions'''

