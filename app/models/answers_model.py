'''app/models/answers_model.py'''
import os
import psycopg2
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class AnswersModel(object):
    '''answers class model'''
    def __init__(self):
        '''open database connections'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def check_if_question_exists(self, question_id):
        '''helper method to check if a question exists'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True
        
    def post_answer(self,question_id, content, username):
        '''post an answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        self.cursor.execute("SELECT answer_id, a_username FROM answers WHERE a_content = (%s);", (content, ))
        result = self.cursor.fetchone()
        if result:
            if result[1] == username:
                self.conn.close()
                return dict(message="You have already posted this answer. To edit answer vist question #" + 
                            str(question_id) + " answer #" + str(result[0]), question_id=question_id, answer_id=result[0], error=409)
        sql = "INSERT INTO answers (q_id, a_content, a_username) VALUES (%s, %s, %s) RETURNING answer_id;"
        self.cursor.execute(sql,(question_id, content, username))
        a_id = self.cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        if not a_id:
            return dict(message="Failed to post answer. Try again.", error=404)
        return dict(message="Answer Posted!")

    def get_all_answers_to_question(self, question_id):
        '''get all answers to a question'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        self.cursor.execute("SELECT * FROM answers WHERE q_id = (%s) ORDER BY accepted DESC;", (question_id,))
        result2 = self.cursor.fetchall()
        if not result2:
            return dict(message="No answers at the moment")
        return result2

    def update_or_accept_answer(self, question_id, answer_id, username, content, action):
        '''Update or accept answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        self.cursor.execute("SELECT * FROM answers WHERE answer_id = (%s);", (answer_id,))
        result2 = self.cursor.fetchone()
        if not result2:
            self.conn.close()
            return dict(message="This answer doesn't exist", error=404) 
        if action == "update":
            if username == result2[3]:
                self.cursor.execute("UPDATE answers SET a_content = (%s) WHERE answer_id = (%s);", (content, answer_id,))
                self.conn.commit()
                self.conn.close()
                return dict(message="Answer updated!")
            return dict(message="Unauthorized to edit answer", error=401)
            
        self.cursor.execute("SELECT q_username FROM questions WHERE question_id = (%s);", (question_id,))
        u_name = self.cursor.fetchone()[0]
        if username != u_name:
            return dict(message="Unauthorized to accept answer", error=401)
        self.cursor.execute("UPDATE answers SET accepted = (%s) WHERE accepted = (%s);", (0, 1,))
        self.cursor.execute("UPDATE answers SET accepted = (%s) WHERE answer_id = (%s);", (1, answer_id,))
        self.cursor.execute("UPDATE questions SET q_accepted_answer = (%s) WHERE question_id = (%s);", (answer_id, question_id,))
        self.conn.commit()
        self.conn.close()
        return dict(message="Answer #" + str(answer_id) + " accepted!")
        