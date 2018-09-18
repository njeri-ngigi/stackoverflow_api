'''test/test_upvote_downvote.py'''
import json
from tests.base_test import BaseTest

class TestQuestionAnswers(BaseTest):
    '''Class Testing Question Answers'''
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
