'''views/questions.py'''
import ast
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app.models.questions_model import QuestionsModel
from app.models.answers_model import AnswersModel
from app.models.vote_model import VoteModel
from app.views.validate import Validate

validate = Validate()

class Questions(Resource):
    '''class representing retrieving all questions and posting questing endpoint'''
    @classmethod
    def get(cls):
        '''get all questions'''
        limit = request.args.get('limit')
        if limit:
            limit = ast.literal_eval(limit)
        query = request.args.get('query')
        pages = request.args.get('pages')
        if pages:
            pages = ast.literal_eval(pages)
        my_question = QuestionsModel()
        if query == "most_answers":
            result = my_question.get_all_questions(limit, pages, most_answers=True)
        else:
            result = my_question.get_all_questions(limit, pages)
        all_questions = []
        for i in result:
            question = dict(id=i[0], title=i[1], content=i[2], username=i[3], answers_given=i[5])
            all_questions.append(question)
        return all_questions, 200

    @classmethod
    @jwt_required
    def post(cls):
        '''post a question'''
        data = request.get_json()
        result = validate.check_for_data(data)
        if not result:
            title = data.get("title")
            content = data.get("content")
            result = validate.check_for_content([title, content])
            if not result:
                result = validate.check_for_white_spaces([title, content])
                if not result:
                    result = validate.check_for_length(title)
                    if not result:
                        username = get_jwt_identity()
                        my_question = QuestionsModel()
                        result2 = my_question.post_question(title, content, username)
                        return result2["response"], result2["status_code"]
        return result, 400

class QuestionsQuestionId(Resource):
    '''Class respresenting activities for a single question'''
    @classmethod
    def get(cls, question_id):
        '''get single question'''
        q_id = ast.literal_eval(question_id)
        my_question = QuestionsModel()
        result = my_question.get_single_question(q_id)
        return result["response"], result["status_code"]

    @classmethod
    @jwt_required
    def delete(cls, question_id):
        '''delete single question'''
        username = get_jwt_identity()
        q_id = ast.literal_eval(question_id)
        my_question = QuestionsModel()
        result = my_question.delete_question(q_id, username)
        return result["response"], result["status_code"]

class QuestionsAnswers(Resource):
    '''Class representing posting an answer endpoint'''
    @classmethod
    @jwt_required
    def post(cls, question_id):
        '''post an answer'''
        data = request.get_json()
        result = validate.check_for_data(data)
        if not result:
            content = data.get("content")
            result = validate.check_for_content([content])
            if not result:
                result = validate.check_for_white_spaces([content])
                if not result:
                    username = get_jwt_identity()
                    q_id = ast.literal_eval(question_id)
                    my_answer = AnswersModel()
                    result2 = my_answer.post_answer(q_id, content, username)
                    return result2["response"], result2["status_code"]
        return result, 400

    @classmethod
    def get(cls, question_id):
        '''get all answers to a question'''
        limit = request.args.get('limit')
        pages = request.args.get('pages')
        if limit:
            limit = ast.literal_eval(limit)
        if pages:
            pages = ast.literal_eval(pages)
        q_id = ast.literal_eval(question_id)
        my_answer = AnswersModel()
        result = my_answer.get_all_answers_to_question(q_id, limit, pages)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        all_answers = []
        for i in result:
            answer = {"id":i[0], "username":i[3], "content":i[2], "upvotes":i[5], "downvotes":i[6]}
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
            result = validate.check_for_content([content])
            if result:
                return result, 400
            result = validate.check_for_white_spaces([content])
            if result:
                return result, 400
            action = "update"
        my_answer = AnswersModel()
        result = my_answer.update_or_accept_answer(q_id, a_id, username, content, action)
        return result["response"], result["status_code"]

class QuestionsAnswersUpvote(Resource):
    '''class represting upvoting an answer'''
    def __init__(self):
        self.action = "upvote"
    @jwt_required
    def post(self, question_id, answer_id):
        '''post method (upvote answer)'''
        q_id = ast.literal_eval(question_id)
        a_id = ast.literal_eval(answer_id)
        username = get_jwt_identity()
        my_vote = VoteModel()
        result = my_vote.upvote_or_downvote(q_id, a_id, username, self.action)
        return result["response"], result["status_code"]

class QuestionsAnswersDownvote(QuestionsAnswersUpvote):
    '''class represting downvoting an answer'''
    def __init__(self):
        self.action = "downvote"

class UserQuestions(Resource):
    '''class representing get all user questions'''
    @classmethod
    @jwt_required
    def get(cls):
        '''get all user's questions'''
        limit = request.args.get('limit')
        pages = request.args.get('pages')
        if limit:
            limit = ast.literal_eval(limit)
        if pages:
            pages = ast.literal_eval(pages)
        username = get_jwt_identity()
        my_question = QuestionsModel()
        result = my_question.get_all_user_questions(username, limit, pages)
        all_questions = []
        for i in result:
            question = {"question_id": i[0], "title": i[1], "content": i[2], "answers": i[5]}
            all_questions.append(question)
        return all_questions, 200

class UserAnswers(Resource):
    '''class representing get all user answers'''
    @classmethod
    @jwt_required
    def get(cls):
        '''get all user's answers'''
        username = get_jwt_identity()
        my_question = QuestionsModel()
        return my_question.get_all_user_answers(username)

class SearchQuestion(Resource):
    '''class representing search question'''
    @classmethod
    def post(cls):
        '''search question'''
        limit = request.args.get('limit')
        if not limit:
            return dict(message="Enter a limit to search through"), 400
        limit = ast.literal_eval(limit)
        data = request.get_json()
        result = validate.check_for_data(data)
        if not result:
            content = data.get("content")
            result = validate.check_for_content([content])
            if not result:
                result = validate.check_for_white_spaces([content])
                if not result:
                    my_question = QuestionsModel()
                    result2 = my_question.search_question(content, limit)
                    return result2["response"], result2["status_code"]
        return result, 400
