'''app/models.py'''
import os
import psycopg2
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

ALL_USERS = {}
ALL_QUESTIONS = []

class Question(object):
    '''Question class model'''
    def __init__(self, u_title, u_content, u_username):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    @classmethod
    def get_all_questions(cls):
        '''get all questions'''
        return ALL_QUESTIONS

    @classmethod
    def get_single_question(cls, question_id):
        '''get single question'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        return dict(question=ALL_QUESTIONS[question_id])

class User(object):
    '''User class model'''
    def __init__(self):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def add_user(self, name, username, email, password):
        '''Add a user'''
        pw_hash = generate_password_hash(password)
        # check if username already exists
        self.cursor.execute("select * from users where username = (%s);", (username,))
        result = self.cursor.fetchone()
        if not result:
            sql = """INSERT INTO users(name, username, email, password)
                     VALUES(%s, %s, %s, %s);"""
            self.cursor.execute(sql, (name, username, email, pw_hash))
            self.conn.commit()
            # check that user was signed up
            self.cursor.execute("select * from users where username = (%s);", (username,))
            result2 = self.cursor.fetchone()
            self.conn.close()
            if not result2:
                return dict(message="Failed to signup, try again.", error=404)
            return dict(message="Welcome " + username + "!")
        self.conn.close()
        return dict(message="Username already exists. Try a different one.")

    def login(self, username, password):
        '''login user'''
        self.cursor.execute("SELECT username, password FROM users WHERE username = (%s);", (username,))
        result = self.cursor.fetchone()
        self.conn.close()
        if not result:
            return dict(message="Username doesn't exixt. Try Signing up.", error=401)
        is_password_correct = check_password_hash(result[1], password)
        if is_password_correct:
            return dict(message="Welcome back, " + username + "!")
        return dict(message="Incorrect password", error=401)

    @classmethod
    def post_answer(cls, question_id, username, content):
        '''Post answer'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        question.answers.append({username:content})
        return dict(message="Answer Posted!")

    @classmethod
    def delete_question(cls, question_id, username):
        '''Delete question'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        u_question = ALL_QUESTIONS[question_id]
        if u_question.username != username:
            return dict(message="Unauthorized to delete this question", error=401)
        ALL_QUESTIONS.pop(question_id)
        return dict(message="Question " + "#" + str(question_id) + " Deleted Successfully")

    @classmethod
    def update_answer(cls, question_id, answer_id, username, content):
        '''Update answer'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        if answer_id >= len(question.answers):
            return dict(message="This answer doesn't exist", error=404)
        answer = question.answers[answer_id]
        if username not in answer:
            return dict(message="Unauthorized to edit answer", error=401)
        answer[username] = content
        return dict(message="Answer updated!")

    @classmethod
    def accept_answer(cls, question_id, answer_id, username):
        '''Accept answer'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        if username != question.username:
            return dict(message="Unauthorized to accept answer", error=401)
        if answer_id >= len(question.answers):
            return dict(message="This answer doesn't exist", error=404)
        question.answer_accepted = answer_id
        return dict(message="Answer #" + str(answer_id) + " accepted!")
