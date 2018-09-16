import os
import json
import unittest
import psycopg2
from app.application import create_app
from instance.config import app_config

class BaseTest(unittest.TestCase):
    '''Class Testing Question Answers'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        #signup 3 users
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "User", "username": "user1",
                                            "email": "user1@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "User", "username": "user2",
                                            "email": "user2@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Commenter", "username": "commenter",
                                            "email": "commenter@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Voter", "username": "voter",
                                            "email": "voter@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        #login in all users
        res = self.client().post('/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps({"username": "user1", "password": "Test123"}))
        u_data = json.loads(res.data)
        self.a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "user2", "password": "Test123"}))
        u_data2 = json.loads(res2.data)
        self.a_token2 = u_data2["token"]

        res3 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "commenter", "password": "Test123"}))
        u_data3 = json.loads(res3.data)
        self.a_token3 = u_data3["token"]
        #user1 posts 3 questions
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Sample title 1",
                                            "content": "Sample content"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Sample title 2",
                                            "content": "Sample content 2"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Sample title 3",
                                            "content": "Sample content 3"}))
        #user2 posts 2 answers
        self.client().post('/api/v1/questions/1/answers',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample answer 1"}))
        self.client().post('/api/v1/questions/1/answers',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample answer 2"}))
        #commenter posts a comment
        self.client().post('/api/v1/questions/1/answers/1/comments',
                           headers=dict(Authorization="Bearer " + self.a_token3),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample comment 1"}))

    def tearDown(self):
        current_environemt = os.environ['ENV']
        conn_string = app_config[current_environemt].CONNECTION_STRING
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE votes, comments, answers, questions, revoked_tokens, users")
        conn.commit()
        conn.close()