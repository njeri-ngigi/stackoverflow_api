'''tests/test_questions.py'''
import os
import unittest
import json
import psycopg2
from app.application import create_app
from instance.config import app_config

class TestQuestions(unittest.TestCase):
    '''Class testing questions'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        #register 2 users
        self.client().post('/api/v1/auth/signup', content_type="application/json",
                           data=json.dumps({"name": "Njeri", "username": "njery",
                                            "email": "njeri@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup', content_type="application/json",
                           data=json.dumps({"name": "Suite", "username": "suite",
                                            "email": "suite@to.com", "password": "Test123",
                                            "confirm_password": "Test123"}))
        self.client().post('/api/v1/auth/signup', content_type="application/json",
                           data=json.dumps({"name": "User", "username": "user",
                                            "email": "user@to.com", "password": "Test123",
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
                                  data=json.dumps({"username": "user", "password": "Test123"}))
        u_data3 = json.loads(res3.data)
        self.a_token3 = u_data3["token"]
        #post 3 questions
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token),
                           content_type="application/json",
                           data=json.dumps({"title": "Git branching",
                                            "content": "How to create, checkout a branch in git"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"title": "How to make a github page?",
                                            "content": "How to host html using github pages"}))
        self.client().post('/api/v1/questions',
                           headers=dict(Authorization="Bearer " + self.a_token2),
                           content_type="application/json",
                           data=json.dumps({"title": "Baby Shower",
                                            "content": "How to throw a greate baby shower"}))
    def test_post_questions(self):
        '''test handling posting questions'''
        #successfull post question
        result = self.client().post('/api/v1/questions',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"title": "Baking a sponge cake",
                                                     "content": "How many eggs to put in cake"}))
        result2 = self.client().post('/api/v1/questions',
                                     headers=dict(Authorization="Bearer " + self.a_token),
                                     content_type="application/json",
                                     data=json.dumps({"title": "Baking a sponge cake",
                                                      "content": "How many eggs to put in cake"}))
        #post question with the same title
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Baking a sponge cake, Posted!", my_data["message"])

        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("Question has already been asked. Visit question #4", my_data2["message"])
        #test whitespaces
        result3 = self.client().post('/api/v1/questions',
                                     headers=dict(Authorization="Bearer " + self.a_token),
                                     content_type="application/json",
                                     data=json.dumps({"title": "  ",
                                                      "content": "  "}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).", my_data3["message"])
        #test empty input fields
        result4 = self.client().post('/api/v1/questions',
                                     headers=dict(Authorization="Bearer " + self.a_token),
                                     content_type="application/json",
                                     data=json.dumps({}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data4["message"])
        #test for missing content and title
        result5 = self.client().post('/api/v1/questions',
                                     headers=dict(Authorization="Bearer " + self.a_token),
                                     content_type="application/json",
                                     data=json.dumps({"title": "",
                                                      "content": ""}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Title or Content fields missing", my_data5["message"])

    def test_get_questions(self):
        '''test getting all questions and single questions'''
        #test get all questions
        result = self.client().get('/api/v1/questions')
        my_data = json.loads(result.data)
        self.assertGreaterEqual(len(my_data), 0)
        self.assertEqual(result.status_code, 200)
        #test get single question
        result2 = self.client().get('/api/v1/questions/1')
        my_data2 = json.loads(result2.data)
        self.assertEqual("Git branching", my_data2["title"])
        self.assertEqual(result2.status_code, 200)
        #test missing question
        result3 = self.client().get('/api/v1/questions/10')
        my_data3 = json.loads(result3.data)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        self.assertEqual(result3.status_code, 404)
        #test limit
        result4 = self.client().get('/api/v1/questions?limit=1')
        my_data4 = json.loads(result4.data)
        self.assertEqual(len(my_data4), 1)
        self.assertEqual(result4.status_code, 200)
        #test get questions with most answers with limit
        result5 = self.client().get('/api/v1/questions?limit=1&query=most_answers')
        my_data5 = json.loads(result5.data)
        self.assertEqual(len(my_data5), 1)
        self.assertEqual(result5.status_code, 200)
        #test get questions with most answers
        result6 = self.client().get('/api/v1/questions?query=most_answers')
        my_data6 = json.loads(result6.data)
        self.assertGreaterEqual(len(my_data6), 0)
        self.assertEqual(result6.status_code, 200)

    def test_delete_questions(self):
        '''test deleting questions'''
        #test successful delete
        result = self.client().get('/api/v1/questions')
        my_data = json.loads(result.data)
        current_length = len(my_data)

        result2 = self.client().delete('/api/v1/questions/2',
                                       headers=dict(Authorization="Bearer " + self.a_token2))
        my_data2 = json.loads(result2.data)
        self.assertEqual("Question #2 Deleted Successfully", my_data2["message"])
        self.assertEqual(result2.status_code, 200)

        result3 = self.client().get('/api/v1/questions')
        my_data3 = json.loads(result3.data)
        self.assertEqual(len(my_data3), current_length-1)

        #test unauthorized delete
        result4 = self.client().delete('/api/v1/questions/1',
                                       headers=dict(Authorization="Bearer " + self.a_token2))
        my_data4 = json.loads(result4.data)
        self.assertEqual("Unauthorized to delete this question", my_data4["message"])
        self.assertEqual(result4.status_code, 401)

        #test missing question
        result5 = self.client().delete('/api/v1/questions/10',
                                       headers=dict(Authorization="Bearer " + self.a_token2))
        my_data5 = json.loads(result5.data)
        self.assertEqual("Question doesn't exist", my_data5["message"])
        self.assertEqual(result5.status_code, 404)

    def test_get_user_questions(self):
        '''test getting user questions'''
        #test successful get
        result = self.client().get('/api/v1/users/questions',
                                   headers=dict(Authorization="Bearer " + self.a_token2))
        my_data = json.loads(result.data)
        self.assertGreaterEqual(len(my_data), 0)
        self.assertEqual(result.status_code, 200)
        #test limit
        result2 = self.client().get('/api/v1/users/questions?limit=1',
                                    headers=dict(Authorization="Bearer " + self.a_token2))
        my_data2 = json.loads(result2.data)
        self.assertEqual(len(my_data2), 1)
        self.assertEqual(result2.status_code, 200)
        #test user has no questions
        result3 = self.client().get('/api/v1/users/questions?limit=1',
                                    headers=dict(Authorization="Bearer " + self.a_token3))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 200)
        self.assertEqual(len(my_data3), 0)

    def test_search_question(self):
        '''test searching questions'''
        #successfull serach by title
        result = self.client().post('/api/v1/questions/search?limit=10',
                                    content_type="application/json",
                                    data=json.dumps({"content":"Git branching"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Git branching", my_data["title"])
        #successful search return closest matches
        result2 = self.client().post('/api/v1/questions/search?limit=10',
                                     content_type="application/json",
                                     data=json.dumps({"content":"git branch"}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 200)
        self.assertGreater(len(my_data2), 0)
        #test search without set limit
        result3 = self.client().post('/api/v1/questions/search',
                                     content_type="application/json",
                                     data=json.dumps({"content":"git branch"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("Enter a limit to search through", my_data3["message"])
        #test no match found
        result4 = self.client().post('/api/v1/questions/search?limit=10',
                                     content_type="application/json",
                                     data=json.dumps({"content":"just in time"}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 404)
        self.assertEqual("No matches. Be the first to ask the question?", my_data4["message"])
        #test whitespaces
        result5 = self.client().post('/api/v1/questions/search?limit=10',
                                     content_type="application/json",
                                     data=json.dumps({"content":"  "}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).", my_data5["message"])
        #test empty input fields
        result6 = self.client().post('/api/v1/questions/search?limit=10',
                                     content_type="application/json",
                                     data=json.dumps({}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data6["message"])
        #test for missing content and title
        result7 = self.client().post('/api/v1/questions/search?limit=10',
                                     content_type="application/json",
                                     data=json.dumps({"content":""}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Content field missing", my_data7["message"])

    def tearDown(self):
        current_environemt = os.environ['ENV']
        conn_string = app_config[current_environemt].CONNECTION_STRING
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE votes, comments, answers, questions, revoked_tokens, users")
        conn.commit()
        conn.close()
