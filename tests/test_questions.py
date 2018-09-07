'''tests/test_questions.py'''
import unittest
import json
from app.application import create_app

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
        #login in both users
        res = self.client().post('/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps({"username": "njery", "password": "Test123"}))
        u_data = json.loads(res.data)
        self.a_token = u_data["token"]

        res2 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                  data=json.dumps({"username": "suite", "password": "Test123"}))
        u_data2 = json.loads(res2.data)
        self.a_token2 = u_data2["token"]
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
    def test_questions(self):
        '''test handling posting questions'''
        result = self.client().post('/api/v1/questions',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"title": "Baking a sponge cake",
                                                     "content": "How many eggs to put in cake"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Baking a sponge cake, Posted!", my_data["message"])
        # test missing fields
        result2 = self.client().post('/api/v1/questions',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 400)
        self.assertEqual("Fields cannot be empty", my_data2["message"])
        # test whitespaces
        result3 = self.client().post('/api/v1/questions',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"title":"  ", "content": "  "}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in fields.", my_data3["message"])

    def test_get_questions(self):
        '''test getting all questions and single questions'''
        #test get all questions
        result = self.client().get('/api/v1/questions')
        my_data = json.loads(result.data)
        self.assertGreater(len(my_data), 0)
        self.assertEqual(result.status_code, 200)

        #test get single question
        result2 = self.client().get('/api/v1/questions/0')
        my_data2 = json.loads(result2.data)
        self.assertEqual("Git branching", my_data2["title"])
        self.assertEqual(result2.status_code, 200)

        #test missing question
        result3 = self.client().get('/api/v1/questions/10')
        my_data3 = json.loads(result3.data)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        self.assertEqual(result3.status_code, 404)

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
        result4 = self.client().delete('/api/v1/questions/0',
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
