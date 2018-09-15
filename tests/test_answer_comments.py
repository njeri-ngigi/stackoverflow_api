'''tests/test_answer_comments.py'''
import json
from tests.base_test import BaseTest

class TestQuestionAnswers(BaseTest):
    '''Class Testing Question Answers'''
    def test_post_answer(self):
        '''test handling posting comments'''
        #test successful post comment
        result = self.client().post('/api/v1/questions/1/answers/1/comments',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Sample comment1"}))
        result2 = self.client().post('/api/v1/questions/1/answers/1/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({"content": "Sample comment1"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Comment posted!", my_data["message"])
        #test posting the same comment more than once
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("Comment already noted. To edit comment visit question #1 answer #1 comment #2", my_data2["message"])
        #test missing input
        result3 = self.client().post('/api/v1/questions/1/answers/1/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data3["message"])
        #test missing content
        result4 = self.client().post('/api/v1/questions/1/answers/1/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({"content": ""}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Content field missing", my_data4["message"])
        #test whitespaces
        result5 = self.client().post('/api/v1/questions/1/answers/1/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({"content": "  "}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).", my_data5["message"])
        #test non-existent question
        result6 = self.client().post('/api/v1/questions/10/answers/1/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({"content": "Sample comment1"}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data6["message"])
        #test non-existent answer
        result7 = self.client().post('/api/v1/questions/1/answers/10/comments',
                                     headers=dict(Authorization="Bearer " + self.a_token3),
                                     content_type="application/json",
                                     data=json.dumps({"content": "Sample comment1"}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data7["message"])

    def test_get_answer_comments(self):
        '''test for getting comments for an answer'''
        #test successful fetch
        result = self.client().get('/api/v1/questions/1/answers/1/comments')
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertGreaterEqual(len(my_data), 0)
        #test non-existent question
        result2 = self.client().get('/api/v1/questions/10/answers/1/comments')
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data2["message"])
        #test non-existent answer
        result3 = self.client().get('/api/v1/questions/1/answers/10/comments')
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data3["message"])
        #test limit
        self.client().post('/api/v1/questions/1/answers/1/comments',
                           headers=dict(Authorization="Bearer " + self.a_token3),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample comment2"}))
        self.client().post('/api/v1/questions/1/answers/1/comments',
                           headers=dict(Authorization="Bearer " + self.a_token3),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample comment3"}))
        self.client().post('/api/v1/questions/1/answers/1/comments',
                           headers=dict(Authorization="Bearer " + self.a_token3),
                           content_type="application/json",
                           data=json.dumps({"content": "Sample comment1"}))
        result4 = self.client().get('/api/v1/questions/1/answers/1/comments?limit=2')
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 200)
        self.assertEqual(len(my_data4), 2)

    def test_update_comment(self):
        '''test updating comments'''
        #test successful update
        result = self.client().put('/api/v1/questions/1/answers/1/comments/1',
                                   headers=dict(Authorization="Bearer " + self.a_token3),
                                   content_type="application/json",
                                   data=json.dumps({"content": "Sample updated comment"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Comment updated!", my_data["message"])
        #test unauthorized update
        result2 = self.client().put('/api/v1/questions/1/answers/1/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Sample updated comment"}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 401)
        self.assertEqual("Unauthorized to edit this comment.", my_data2["message"])
        #test non-existent question
        result3 = self.client().put('/api/v1/questions/20/answers/1/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Sample updated comment"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 404)
        self.assertEqual("Question doesn't exist", my_data3["message"])
        #test non-existent answer
        result4 = self.client().put('/api/v1/questions/1/answers/20/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Sample updated comment"}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 404)
        self.assertEqual("This answer doesn't exist", my_data4["message"])
        #test non-existent comment
        result5 = self.client().put('/api/v1/questions/1/answers/1/comments/10',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": "Sample updated comment"}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 404)
        self.assertEqual("Comment doesn't exist", my_data5["message"])
        #test empty input fields
        result6 = self.client().put('/api/v1/questions/1/answers/1/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data6["message"])
        #test missing content
        result7 = self.client().put('/api/v1/questions/1/answers/1/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": ""}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Content field missing", my_data7["message"])
        #test whitespaces
        result8 = self.client().put('/api/v1/questions/1/answers/1/comments/1',
                                    headers=dict(Authorization="Bearer " + self.a_token3),
                                    content_type="application/json",
                                    data=json.dumps({"content": "  "}))
        my_data8 = json.loads(result8.data)
        self.assertEqual(result8.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).", my_data8["message"])
