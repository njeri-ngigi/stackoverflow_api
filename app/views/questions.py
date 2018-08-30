from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_raw_jwt, get_jwt_claims, get_jwt_identity)
import ast

from app import User, Question

class Questions(Resource):
    def get(self):
        result = Question.getAllQuestions()
        if len(result) == 0:
            return result, 200
        all_questions = []
        for i in result:
            question = dict(title=i.title, content=i.content, username=i.username)
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
        result = dict(title=q.title, content=q.content, username=q.username)
        
        return result, 200

    @jwt_required
    def delete(self, question_id):
        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        result = User.deleteQuestion(q_id, username)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200
