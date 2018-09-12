'''test/test_upvote_downvote.py'''
import os
import unittest
import json
import psycopg2
from app.application import create_app
from instance.config import app_config

class TestQuestionAnswers(unittest.TestCase):
    '''Class Testing Question Answers'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        #signup 3 users
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
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Voter", "username": "voter",
                                            "email": "voter@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        #login in all users
        res = self.client().post('/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps({"username": "njery", "password": "Test123"}))
        u_data = json.loads(res.data)
        self.a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "suite", "password": "Test123"}))
        u_data2 = json.loads(res2.data)
        self.a_token2 = u_data2["token"]

        res3 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "voter", "password": "Test123"}))
        u_data3 = json.loads(res3.data)
        self.a_token3 = u_data3["token"]
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
        #user2 posts answer
        self.client().post('/api/v1/questions/1/answers',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"content": "Use git branch <branch_name>"}))

    def test_upvote_downvote_answer(self):
        '''test upvote'''
        #successful upvote
        result = self.client().post('/api/v1/questions/1/answers/1/upvote',
                                    headers=dict(Authorization="Bearer " + self.a_token3))
        result2 = self.client().post('/api/v1/questions/1/answers/1/upvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Thanks for contributing!", my_data["message"])
        #test user upvoting more than once
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Upvote already noted.", my_data2["message"])
        #non-existent question
        result3 = self.client().post('/api/v1/questions/100/answers/1/upvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        #non-exitent answer
        result4 = self.client().post('/api/v1/questions/1/answers/100/upvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data4["message"])
        #test user voting on their own answer
        result4 = self.client().post('/api/v1/questions/1/answers/1/upvote',
                                     headers=dict(Authorization="Bearer " + self.a_token2))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 401)
        self.assertEqual("You cannot vote on your own answer.", my_data4["message"])

    def test_downvote_answer(self):
        '''test downvote'''
        #successful downvote
        result = self.client().post('/api/v1/questions/1/answers/1/downvote',
                                    headers=dict(Authorization="Bearer " + self.a_token3))
        result2 = self.client().post('/api/v1/questions/1/answers/1/downvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Thanks for contributing!", my_data["message"])
        #test user downvoting more than once
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Downvote already noted.", my_data2["message"])
        #non-existent question
        result3 = self.client().post('/api/v1/questions/100/answers/1/downvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        #non-exitent answer
        result4 = self.client().post('/api/v1/questions/1/answers/100/downvote',
                                     headers=dict(Authorization="Bearer " + self.a_token3))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data4["message"])
        #test user voting on their own answer
        result5 = self.client().post('/api/v1/questions/1/answers/1/downvote',
                                     headers=dict(Authorization="Bearer " + self.a_token2))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 401)
        self.assertEqual("You cannot vote on your own answer.", my_data5["message"])

    def tearDown(self):
        current_environemt = os.environ['ENV']
        conn_string = app_config[current_environemt].CONNECTION_STRING
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE votes, comments, answers, questions, revoked_tokens, users")
        conn.commit()
        conn.close()
