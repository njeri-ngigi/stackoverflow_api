'''views/questions.py'''
import ast
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app.models1 import User, Question
from app.models.questions_model import QuestionsModel

class Questions(Resource):
    '''class representing retrieving all questions and posting questing endpoint'''
    @classmethod
    def get(cls):
        '''get all questions'''
        my_question = QuestionsModel()
        result = my_question.get_all_questions()
        if not result:
            return result, 200
        all_questions = []
        for i in result:
            question = dict(id=i[0], title=i[1], content=i[2], username=i[3])
            all_questions.append(question)
        return all_questions, 200

    @classmethod
    @jwt_required
    def post(cls):
        '''post a question'''
        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty"), 400
        title = data.get("title")
        content = data.get("content")
        if not title or not content:
            return dict(message="Title or Content fields missing"), 400
        #check for whitespaces
        title = title.strip()
        content = content.strip()
        if not title or not content:
            return dict(message="Enter valid data")
            
        username = get_jwt_identity()
        my_question = QuestionsModel()
        result = my_question.post_question(title, content, username)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return dict(message=result["title"] + ", Posted!"), 201

class QuestionsQuestionId(Resource):
    '''Class respresenting activities for a single question'''
    @classmethod
    def get(cls, question_id):
        '''get single question'''
        q_id = ast.literal_eval(question_id)
        my_question = QuestionsModel()
        result = my_question.get_single_question(q_id)
        if "message" in result:
            return dict(message=result["message"]), result["error"]
        return dict(title=result[1], content=result[2], username=result[3]), 200

    @classmethod
    @jwt_required
    def delete(cls, question_id):
        '''delete single question'''
        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        my_question = QuestionsModel()
        result = my_question.delete_question(q_id, username)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200

class QuestionsAnswers(Resource):
    '''Class representing posting an answer endpoint'''
    @classmethod
    @jwt_required
    def post(cls, question_id):
        '''post answer'''
        data = request.get_json()
        if not data:
            return dict(message="Field(s) cannot be empty")
        content = data.get("content")
        if not content:
            return dict(message="Please enter answer content")
        #check for whitespaces
        content = content.strip()
        if not content:
            return dict(message="Enter valid data")

        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        result = User.post_answer(q_id, username, content)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 201

class QuestionsAnswersId(Resource):
    '''class representing activities for a question's answers'''
    @classmethod
    @jwt_required
    def put(cls, question_id, answer_id):
        '''put method'''
        data = request.get_json()
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        #Update an answer
        if data:
            content = data.get("content")
            if not content:
                return dict(message="Please enter answer content")
            result = User.update_answer(q_id, a_id, username, content)
            if "error" in result:
                return dict(message=result["message"]), result["error"]
            return result, 200
        #Accept an answer
        result2 = User.accept_answer(q_id, a_id, username)
        if "error" in result2:
            return dict(message=result2["message"]), result2["error"]
        return result2, 200
