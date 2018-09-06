import os
import psycopg2
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class QuestionsModel(object):
    '''User class model'''
    def __init__(self):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def post_question(self, title, content, username):
        '''Post a question'''
        sql = """INSERT INTO questions(q_title, q_content, q_username)
                 VALUES(%s, %s, %s);"""
        self.cursor.execute(sql, (title, content, username))
        self.conn.commit()
        self.cursor.execute("SELECT q_title FROM questions WHERE q_title = (%s);", (title,))
        result = self.cursor.fetchone()
        if not result:
            return dict(message="Failed to add question. Try again.", error=404)
        return dict(title=title)