import unittest
import json
import ast
from app import createApp

class TestQuestionAnswers(unittest.TestCase):
    def setUp(self):
        self.app = createApp(config_name="testing")
        self.client = self.app.test_client

        #signup 2 users
        self.client().post('/api/v1/auth/signup', content_type="application/json", data=json.dumps({"name": "Njeri", "username": "njery", 
                            "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup', content_type="application/json", data=json.dumps({"name": "Suite", "username": "suite", 
                            "email": "suite@to.com", "password": "Test123", "confirm_password": "Test123"}))        
        #login in both users
        res = self.client().post('/api/v1/auth/login', content_type="application/json", 
                            data=json.dumps({"username": "njery", "password": "Test123"}))
        u_data = ast.literal_eval(res.data)
        self.a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json", 
                            data=json.dumps({"username": "suite", "password": "Test123"}))
        u_data2 = ast.literal_eval(res2.data)
        self.a_token2 = u_data2["token"]
        #user1 posts a question
        self.client().post('/api/v1/questions', headers=dict(Authorization="Bearer " + self.a_token), content_type="application/json",
                            data=json.dumps({"title": "Git branching", "content": "How to create and checkout a branch in git"}))

    def test_post_answer(self):
        '''test handling posting an answer'''
        result = self.client().post('/api/v1/questions/0/answers', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "Use git branch <branch_name>. The checkout the branch using git checkout <branch_name>"}))
        my_data = ast.literal_eval(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Answer Posted!", my_data["message"])

        #test non-exixtent question
        result2 = self.client().post('/api/v1/questions/20/answers', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "Use git branch <branch_name>. The checkout the branch using git checkout <branch_name>"}))
        my_data2 = ast.literal_eval(result2.data)
        self.assertEqual(result2.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data2["message"])

    def test_accept_answer(self):
        '''test accepting answer'''

    def test_update_answer(self):
        '''test updating answer'''
