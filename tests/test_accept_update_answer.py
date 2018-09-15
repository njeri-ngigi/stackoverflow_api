'''tests/test_accept_update_answer.py'''
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

        #user1 posts a questions
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Sample title",
                                            "content": "Sample content"}))
        #user2 posts answer
        self.client().post('/api/v1/questions/1/answers',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample answer 1"}))

    def test_accept_update_answer(self):
        '''test accepting and updating answer'''
        #test successful accept answer
        result = self.client().put('/api/v1/questions/1/answers/1',
                                   headers=dict(Authorization="Bearer " + self.a_token),
                                   content_type="application/json",
                                   data=json.dumps({}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Answer #1 accepted!", my_data["message"])
        #test unauthorized accepting of answer
        result2 = self.client().put('/api/v1/questions/1/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 401)
        self.assertEqual("Unauthorized to accept answer", my_data2["message"])
        #test successful update answer
        result3 = self.client().put('/api/v1/questions/1/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 200)
        self.assertEqual("Answer updated!", my_data3["message"])
        #test unauthorized updating answer
        result4 = self.client().put('/api/v1/questions/1/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 401)
        self.assertEqual("Unauthorized to edit answer", my_data4["message"])
        #test question doesn't exist
        result5 = self.client().put('/api/v1/questions/10/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data5["message"])
        #test answer doesn't exist
        result6 = self.client().put('/api/v1/questions/1/answers/10',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "2 tsp per 3 cups of flour"}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data6["message"])
        #check for whitespaces in update input content
        result7 = self.client().put('/api/v1/questions/1/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": "  "}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).",
                         my_data7["message"])
        #missing input content field
        result8 = self.client().put('/api/v1/questions/1/answers/1',
                                    headers=dict(Authorization="Bearer " + self.a_token2),
                                    content_type="application/json",
                                    data=json.dumps({"content": ""}))
        my_data8 = json.loads(result8.data)
        self.assertEqual(result8.status_code, 400)
        self.assertEqual("Content field missing", my_data8["message"])

    def tearDown(self):
        current_environemt = os.environ['ENV']
        conn_string = app_config[current_environemt].CONNECTION_STRING
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE votes, comments, answers, questions, revoked_tokens, users")
        conn.commit()
        conn.close()
