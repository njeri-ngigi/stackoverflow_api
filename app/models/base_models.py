'''app/models/base_models.py'''
import os
import psycopg2
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class BaseModel(object):
    '''answers class model'''
    def __init__(self):
        '''open database connections'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def check_if_question_exists(self, question_id):
        '''check if question exists'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        if not result:
            return dict(response=dict(message="Question doesn't exist"), status_code=404)
        return True

    def check_if_answer_exists(self, answer_id):
        '''check if an answer exists'''
        self.cursor.execute("SELECT * FROM answers WHERE answer_id = (%s);", (answer_id,))
        result = self.cursor.fetchone()
        if not result:
            return dict(response=dict(message="This answer doesn't exist"), status_code=404)
        return result

    def paginate(self, my_list, page):
        '''get a page of results'''
        num = 5
        end = num * page
        start = end - num
        if start < 0:
            start = 0
        return my_list[start:end]
        