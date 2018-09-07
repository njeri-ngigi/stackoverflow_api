'''app/models/questions_model.py'''
import os
import psycopg2
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class QuestionsModel(object):
    '''questions class model'''
    def __init__(self):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def post_question(self, title, content, username):
        '''Post a question'''
        sql = """INSERT INTO questions(q_title, q_content, q_username)
                 VALUES(%s, %s, %s) RETURNING question_id;"""
        self.cursor.execute(sql, (title, content, username))
        q_id = self.cursor.fetchone()[0]
        self.conn.commit()
        self.cursor.close()
        if not q_id:
            return dict(message="Failed to add question. Try again.", error=404)
        return dict(title=title)

    def get_all_questions(self):
        '''get all questions'''
        self.cursor.execute("SELECT * FROM questions")
        result = self.cursor.fetchall()
        self.conn.close()
        return result

    def get_single_question(self, question_id):
        '''get single question'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        self.conn.close()
        if not result:
            return dict(message="Question doesn't exist", error=404)
        return result

    def delete_question(self, question_id, username):
        '''Delete question'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        if username != result[3]:
            self.conn.close()
            return dict(message="Unauthorized to delete this question", error=401)
        self.cursor.execute("DELETE FROM questions WHERE question_id = (%s);", (question_id,))
        self.conn.commit()
        # check if question is deleted
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result2 = self.cursor.fetchone()
        self.conn.close()
        if result2:
            return dict(message="Failed to delete question. Try again.")
        return dict(message="Question " + "#" + str(question_id) + " Deleted Successfully")