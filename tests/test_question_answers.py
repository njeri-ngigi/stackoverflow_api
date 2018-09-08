'''tests/test_question_answers.py'''
import os
import psycopg2
import unittest
import json

from app.application import create_app
from instance.config import app_config

class TestQuestionAnswers(unittest.TestCase):
    '''Class Testing Question Answers'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        #signup 2 users
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Njeri", "username": "njery",
                                            "email": "njeri@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Suite", "username": "suite",
                                            "email": "suite@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        #login in both users
        res = self.client().post('/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps({"username": "njery", "password": "Test123"}))
        u_data = json.loads(res.data)
        self.a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "suite", "password": "Test123"}))
        u_data2 = json.loads(res2.data)
        self.a_token2 = u_data2["token"]
        #user1 posts 3 questions
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Git branching",
                                            "content": "How to create & checkout a branch in git"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Baking",
                                            "content": "How much baking soda to use?"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Sample",
                                            "content": "Content"}))
        #user2 posts answer
        self.client().post('/api/v1/questions/1/answers',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Use git branch <branch_name>"}))
    def test_post_answer(self):
        '''test handling posting an answer'''
        #test successful post
        result = self.client().post('/api/v1/questions/1/answers',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Use git checkout branch <branch_name>"}))
        #test repeated answer
        result2 = self.client().post('/api/v1/questions/1/answers',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Use git checkout branch <branch_name>"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Answer Posted!", my_data["message"])

        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("You have already posted this answer. To edit answer vist question #1 answer #2", my_data2["message"])
        #test non-exixtent question
        result3 = self.client().post('/api/v1/questions/20/answers',
                                     headers=dict(Authorization="Bearer " + self.a_token2),
                                     content_type="application/json",
                                     data=json.dumps({"content": "Use git branch <branch_name>"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        #test whitespaces
        result4 = self.client().post('/api/v1/questions/20/answers',
                                     headers=dict(Authorization="Bearer " + self.a_token2),
                                     content_type="application/json",
                                     data=json.dumps({"content": "  "}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in fields.", my_data4["message"])
        #test missing input data
        result5 = self.client().post('/api/v1/questions/20/answers',
                                     headers=dict(Authorization="Bearer " + self.a_token2),
                                     content_type="application/json",
                                     data=json.dumps({}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data5["message"])
        #test missing input data fields
        result6 = self.client().post('/api/v1/questions/20/answers',
                                     headers=dict(Authorization="Bearer " + self.a_token2),
                                     content_type="application/json",
                                     data=json.dumps({"content": ""}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Please enter answer content", my_data6["message"])
    
    def test_get_all_answers_to_question(self):
        '''test handling getting all answers to a question'''
        #successful get
        result = self.client().get('/api/v1/questions/1/answers')
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertGreater(len(my_data), 0)
        #test no answers
        result2 = self.client().get('/api/v1/questions/3/answers')
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("No answers at the moment", my_data2["message"])
        #non-existent question
        result3 = self.client().get('/api/v1/questions/31/answers')
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data3["message"])


    def test_accept_update_answer(self):
        '''test accepting and updating answer'''
        #user2 posts answer
        self.client().post('/api/v1/questions/2/answers',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"content": "1 tsp per 3 cups of flour"}))
        #test successful accept answer
        result = self.client().put('/api/v1/questions/2/answers/1',
                                   headers=dict(Authorization="Bearer " + self.a_token),
                                   content_type="application/json",
                                   data=json.dumps({}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Answer #1 accepted!", my_data["message"])
        #test unauthorized accepting of answer
        result2 = self.client().put('/api/v1/questions/2/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 401)
        self.assertEqual("Unauthorized to accept answer", my_data2["message"])
        #test successful update answer
        result3 = self.client().put('/api/v1/questions/2/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 200)
        self.assertEqual("Answer updated!", my_data3["message"])
        #test unauthorized updating answer
        result4 = self.client().put('/api/v1/questions/2/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 401)
        self.assertEqual("Unauthorized to edit answer", my_data4["message"])
        #test question doesn't exist
        result5 = self.client().put('/api/v1/questions/10/answers/0',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data5["message"])
        #test answer doesn't exist
        result6 = self.client().put('/api/v1/questions/2/answers/10',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data6["message"])
        #check for whitespaces in update input content
        result7 = self.client().put('/api/v1/questions/2/answers/10',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "  "}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in fields.", my_data7["message"])
        #missing input content field
        result8 = self.client().put('/api/v1/questions/2/answers/10',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": ""}))
        my_data8 = json.loads(result8.data)
        self.assertEqual(result8.status_code, 400)
        self.assertEqual("Please enter answer content", my_data8["message"])
    
    def tearDown(self):
        current_environemt = os.environ['ENV']
        conn_string = app_config[current_environemt].CONNECTION_STRING
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE answers, questions, revoked_tokens, users")
        conn.commit()
        conn.close()
        