'''views/questions.py'''
import ast
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app.models.questions_model import QuestionsModel
from app.models.answers_model import AnswersModel

class Questions(Resource):
    '''class representing retrieving all questions and posting questing endpoint'''
    @classmethod
    def get(cls):
        '''get all questions'''
        limit = request.args.get('limit')
        if limit:
            limit = ast.literal_eval(limit)
        my_question = QuestionsModel()
        result = my_question.get_all_questions(limit)
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
            return dict(message="Enter valid data. Look out for whitespaces in fields."), 400
            
        username = get_jwt_identity()
        my_question = QuestionsModel()
        result = my_question.post_question(title, content, username)
        if "error" in result:
            return dict(message=result["message"], question_id=result["question_id"]), result["error"]
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
        '''post an answer'''
        data = request.get_json()
        if not data:
            return dict(message="Field(s) cannot be empty"), 400
        content = data.get("content")
        if not content:
            return dict(message="Please enter answer content"), 400
        #check for whitespaces
        content = content.strip()
        if not content:
            return dict(message="Enter valid data. Look out for whitespaces in fields."), 400

        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        my_answer = AnswersModel()
        result = my_answer.post_answer(q_id, content, username)
        if "question_id" in result:
            return dict(message=result["message"], question_id=result["question_id"], 
                        answer_id=result["answer_id"]), result["error"]
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 201

    @classmethod
    def get(cls, question_id):
        '''get all answers to a question'''
        limit = request.args.get('limit')
        if limit:
            limit = ast.literal_eval(limit)
        q_id = ast.literal_eval(question_id)
        my_answer = AnswersModel()
        result = my_answer.get_all_answers_to_question(q_id, limit)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        if "message" in result:
            return result, 200
        all_answers = []
        for i in result:
            answer = {i[3]:i[2]}
            if i[4] == 1:
                answer["accepted"] = "true"
            all_answers.append(answer)
        return all_answers, 200

class QuestionsAnswersId(Resource):
    '''class representing activities for a question's answers'''
    @classmethod
    @jwt_required
    def put(cls, question_id, answer_id):
        '''put method (edit or accept answer)'''
        data = request.get_json()
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        content = ""
        action = "accept"
        if data:
            content = data.get("content")
            if not content:
                return dict(message="Please enter answer content"), 400

            content = content.strip()
            if not content:
                return dict(message="Enter valid data. Look out for whitespaces in fields."), 400
            action = "update" 
        my_answer = AnswersModel()
        result = my_answer.update_or_accept_answer(q_id, a_id, username, content, action) 
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200

class QuestionsAnswersUpvote(Resource):
    '''class represting upvoting an answer'''
    @classmethod
    @jwt_required
    def post(cls, question_id, answer_id):
        '''post method (upvote answer)'''
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        my_answer = AnswersModel()
        result = my_answer.upvote_or_downvote(q_id, a_id, username, "upvote")
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200

class QuestionsAnswersDownvote(Resource):
    '''class represting downvoting an answer'''
    @classmethod
    @jwt_required
    def post(cls, question_id, answer_id):
        '''post method (downvote answer)'''
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        my_answer = AnswersModel()
        result = my_answer.upvote_or_downvote(q_id, a_id, username, "downvote")
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200
    
class UserQuestions(Resource):
    '''class representing get all user questions'''
    @classmethod
    @jwt_required
    def get(cls):
        limit = request.args.get('limit')
        if limit:
            limit = ast.literal_eval(limit)
        username = get_jwt_identity()
        my_question = QuestionsModel()
        result = my_question.get_all_user_questions(username, limit)
        if not result:
            return dict(message="No questions here at the moment. Ask a question?"), 404
        all_questions = []    
        for i in result:
            question={"question_id":i[0], "title":i[1], "content":i[2], "answers":i[4]}
            all_questions.append(question)
        return all_questions, 200

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
        if not data:
            return dict(message="Field cannot be empty"), 400
        content = data.get("content")
        if not content:
            return dict(message="Please enter content"), 400
        content = content.strip()
        if not content:
            return dict(message="Enter valid data. Look out for whitespaces in fields."), 400
        my_answer = AnswersModel()
        result = my_answer.post_comment(q_id, a_id, username, content)
        if "question_id" in result:
            return dict(message=result["message"], question_id=result["question_id"],
                        answer_id=result["answer_id"], comment_id=result["comment_id"]), result["error"]
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 201

    @classmethod
    def get(cls, question_id, answer_id):
        '''get all comments for an answer'''
        limit = request.args.get('limit')
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        if limit:
            limit = ast.literal_eval(limit)
        my_answer = AnswersModel()
        result = my_answer.get_answer_comments(q_id, a_id, limit)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        all_comments = []
        for i in result:
            all_comments.append({i[2]:i[3]})
        return all_comments, 200
    
class AnswerCommentsId(Resource):
    '''class representing comment actions'''
    @classmethod
    @jwt_required
    def put(self, question_id, answer_id, comments_id):
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        c_id = ast.literal_eval(comments_id)
        username = get_jwt_identity()
        data = request.get_json()
        if not data:
            return dict(message="Field cannot be empty"), 400
        content = data.get("content")
        if not content:
            return dict(message="Please enter content"), 400
        content = content.strip()
        if not content:
            return dict(message="Enter valid data. Look out for whitespaces in fields."), 400
        my_answer = AnswersModel()
        result = my_answer.update_comment(q_id, a_id, c_id, username, content)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 200
