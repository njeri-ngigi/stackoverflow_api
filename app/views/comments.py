import ast
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.models.answers_model import AnswersModel
from app.views.validate import Validate

validate = Validate()

class AnswerComments(Resource):
    '''class representing comment actions'''
    @classmethod
    @jwt_required
    def post(cls, question_id, answer_id):
        '''post a comment'''
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        data = request.get_json()
        result = validate.check_for_data(data)
        if not result:
            content = data.get("content")
            result = validate.check_for_content([content])
            if not result:
                result = validate.check_for_white_spaces([content])
                if not result:
                    my_answer = AnswersModel()
                    result2 = my_answer.post_comment(q_id, a_id, username, content)
                    return result2["response"], result2["status_code"]
        return result, 400

    @classmethod
    def get(cls, question_id, answer_id):
        '''get all comments for an answer'''
        limit = request.args.get('limit')
        pages = request.args.get('pages')
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        if limit:
            limit = ast.literal_eval(limit)
        if pages:
            pages = ast.literal_eval(pages)
        my_answer = AnswersModel()
        result = my_answer.get_answer_comments(q_id, a_id, limit, pages)
        if "status_code" in result:
            return result["response"], result["status_code"]
        all_comments = []
        for i in result:
            all_comments.append({i[2]:i[3]})
        return all_comments, 200

class AnswerCommentsId(Resource):
    '''class representing update comment'''
    @classmethod
    @jwt_required
    def put(cls, question_id, answer_id, comments_id):
        '''update comment'''
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        c_id = ast.literal_eval(comments_id)
        username = get_jwt_identity()
        data = request.get_json()
        result = validate.check_for_data(data)
        if not result:            
            content = data.get("content")
            result = validate.check_for_content([content])
            if not result:
                result = validate.check_for_white_spaces([content])
                if not result:            
                    my_answer = AnswersModel()
                    result2 = my_answer.update_comment(q_id, a_id, c_id, username, content)
                    return result2["response"], result2["status_code"]
        return result, 400
