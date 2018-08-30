from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_raw_jwt, get_jwt_identity)
import ast

from app import User, Question

class Questions(Resource):
    def get(self):
        result = Question.getAllQuestions()
        if len(result) == 0:
            return result, 200
        all_questions = []
        for i in result:
            question = dict(title=i.title, content=i.content, username=i.username, answers=i.answers, accepted_answer=i.answer_accepted)
            all_questions.append(question)
        return all_questions, 200

    @jwt_required
    def post(self):
        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty"), 400
        title = data.get("title")
        content = data.get("content")
        
        if not title or not content:
            return dict(message=
                    "Title or Content fields missing"), 400
        username = get_jwt_identity()
        
        result = User.postQuestion(title, content, username)
        return dict(message=result["title"] + ", Posted!"), 201


class QuestionsQuestionId(Resource):
    def get(self, question_id):
        q_id = ast.literal_eval(question_id)
        u_question = Question.getSingleQuestion(q_id)
        
        if "message" in u_question:
            return dict(message=u_question["message"]), u_question["error"]
        q = u_question["q"]
        result = dict(title=q.title, content=q.content, username=q.username, answers=q.answers, accepted_answer=q.answer_accepted)
        
        return result, 200

    @jwt_required
    def delete(self, question_id):
        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        result = User.deleteQuestion(q_id, username)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200

class QuestionsAnswers(Resource):
    @jwt_required
    def post(self, question_id):
        data = request.get_json()
        if not data:
            return dict(message="Field(s) cannot be empty")
        content = data.get("content")
        if not content:
            return dict(message="Please enter answer content")
        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        result = User.postAnswer(q_id, username, content)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 201

class QuestionsAnswersId(Resource):
    @jwt_required
    def put(self, question_id, answer_id):
        data = request.get_json()
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
            
        if data: 
            content = data.get("content")
            if not content:
                return dict(message="Please enter answer content")
            result = User.updateAnswer(q_id, a_id, username, content)

            if "error" in result:
                return dict(message=result["message"]), result["error"]
            return result, 200

        result2 = User.acceptAnswer(q_id, a_id, username)
        if "error" in result2:
            return dict(message=result2["message"]), result2["error"]
        return result2, 200
