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
        #user1 posts 2 questions
        self.client().post('/api/v1/questions', headers=dict(Authorization="Bearer " + self.a_token), content_type="application/json",
                            data=json.dumps({"title": "Git branching", "content": "How to create and checkout a branch in git"}))
        self.client().post('/api/v1/questions', headers=dict(Authorization="Bearer " + self.a_token), content_type="application/json",
                            data=json.dumps({"title": "Baking", "content": "How much baking soda to use?"}))

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

    def test_accept_update_answer(self):
        '''test accepting and updating answer'''  
        #user2 posts answer
        self.client().post('/api/v1/questions/1/answers', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "1 tsp per 3 cups of flour"})) 
        #test successful accept answer      
        result = self.client().put('/api/v1/questions/1/answers/0', headers=dict(Authorization="Bearer " + self.a_token), content_type="application/json",
                            data=json.dumps({})) 
        my_data = ast.literal_eval(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Answer #0 accepted!", my_data["message"])
        #test unauthorized accepting of answer
        result2 = self.client().put('/api/v1/questions/1/answers/0', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({})) 
        my_data2 = ast.literal_eval(result2.data)
        self.assertEqual(result2.status_code, 401)
        self.assertEqual("Unauthorized to accept answer", my_data2["message"])
        #test successful update answer
        result3 = self.client().put('/api/v1/questions/1/answers/0', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "2 tsp per 3 cups of flour"})) 
        my_data3 = ast.literal_eval(result3.data)
        self.assertEqual(result3.status_code, 200)
        self.assertEqual("Answer updated!", my_data3["message"])
        
        #test unauthorized updating answer
        result4 = self.client().put('/api/v1/questions/1/answers/0', headers=dict(Authorization="Bearer " + self.a_token), content_type="application/json",
                            data=json.dumps({"content": "2 tsp per 3 cups of flour"})) 
        my_data4 = ast.literal_eval(result4.data)
        self.assertEqual(result4.status_code, 401)
        self.assertEqual("Unauthorized to edit answer", my_data4["message"])
        
        #test question doesn't exist
        result5 = self.client().put('/api/v1/questions/10/answers/0', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "2 tsp per 3 cups of flour"})) 
        my_data5 = ast.literal_eval(result5.data)
        self.assertEqual(result5.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data5["message"])
        #test answer doesn't exist
        result6 = self.client().put('/api/v1/questions/1/answers/10', headers=dict(Authorization="Bearer " + self.a_token2), content_type="application/json",
                            data=json.dumps({"content": "2 tsp per 3 cups of flour"})) 
        my_data6 = ast.literal_eval(result6.data)
        self.assertEqual(result6.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data6["message"])
        