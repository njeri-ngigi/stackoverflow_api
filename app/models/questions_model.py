'''app/models/questions_model.py'''
from difflib import get_close_matches
from itertools import chain
import psycopg2
from app.models.base_models import BaseModel

class QuestionsModel(BaseModel):
    '''questions class model'''
    def post_question(self, title, content, username):
        '''Post a question'''
        self.cursor.execute("SELECT * FROM questions WHERE q_title = (%s);", (title, ))
        result = self.cursor.fetchone()
        if result:
            my_resp = dict(message="Question has already been asked. Visit question #" +
                        str(result[0]), question_id=result[0])
            return dict(response=my_resp, status_code=409)
        sql = """INSERT INTO questions(q_title, q_content, q_username)
                 VALUES(%s, %s, %s) RETURNING question_id;"""
        self.cursor.execute(sql, (title, content, username))
        q_id = self.cursor.fetchone()[0]
        self.conn.commit()
        self.cursor.close()
        if not q_id:
            return dict(response=dict(message="Failed to add question. Try again."), status_code=500)
        return dict(response=dict(message=title + ", Posted!"), status_code=201)

    def get_all_questions(self, limit=None, pages=None, most_answers=None):
        '''get all questions'''
        sql = "SELECT * FROM questions ORDER BY question_id DESC"
        if most_answers:
            sql = "SELECT * FROM questions ORDER BY q_answers DESC"
        self.cursor.execute(sql)
        if limit:
            result = self.cursor.fetchmany(limit)
        if not limit:
            result = self.cursor.fetchall()
        if pages:
            result = self.paginate(result, pages)
        self.conn.close()
        return result
    
    def fetch_answers(self, all_answers):
        answers = []
        for i in all_answers:
            answer = {"id":i[0], "username":i[3], "content":i[2], "upvotes":i[5], "downvotes":i[6]}
            if i[4] == 1:
                answer["accepted"] = "true"
            answers.append(answer)
        return answers

    def get_single_question(self, question_id, username=None):
        '''get single question'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        if not result:
            self.conn.close()
            return dict(response=dict(message="Question doesn't exist"), status_code=404)
        sql = "SELECT * FROM answers WHERE q_id = (%s) ORDER BY accepted DESC"
        self.cursor.execute(sql, (question_id,))
        result2 = self.cursor.fetchall()
        answers = self.fetch_answers(result2)
        if not username:
            self.conn.close()
        return dict(response=dict(id=result[0], title=result[1], content=result[2], username=result[3], answers_count=len(result2), answers=answers), status_code=200)

    def delete_question(self, question_id, username):
        '''Delete question'''
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result = self.cursor.fetchone()
        if not result:
            self.conn.close()
            return dict(response=dict(message="Question doesn't exist"), status_code=404)
        if username != result[3]:
            self.conn.close()
            return dict(response=dict(message="Unauthorized to delete this question"), status_code=401)
        self.cursor.execute("DELETE FROM questions WHERE question_id = (%s);", (question_id,))
        self.conn.commit()
        # check if question is deleted
        self.cursor.execute("SELECT * FROM questions WHERE question_id = (%s);", (question_id,))
        result2 = self.cursor.fetchone()
        self.conn.close()
        if result2:
            return dict(response=dict(message="Failed to delete question. Try again."), status_code=500)
        return dict(response=dict(message="Question " + "#" + str(question_id) + " Deleted Successfully"), status_code=200)

    def get_all_user_questions(self, username, limit=None, pages=None):
        '''get all questions a user has ever asked'''
        self.cursor.execute("SELECT * FROM questions WHERE q_username = (%s) ORDER BY question_id DESC;", (username,))
        if limit:
            result = self.cursor.fetchmany(limit)
        if not limit:
            result = self.cursor.fetchall()
        if pages:
            result = self.paginate(result, pages)
        self.conn.close()
        return result
    
    def get_all_user_answers(self, username):
        '''get all answers a user has ever given'''
        self.cursor.execute("SELECT q_id FROM answers WHERE a_username = (%s)", (username,))
        result = list(chain.from_iterable(self.cursor.fetchall()))
        all_user_answers = len(result)
        questions = set(result)
        answers = []
        for i in questions:
            result = self.get_single_question(i, True)
            if result["status_code"] != 200:
                return result
            answers.append(result["response"]) 
        self.conn.close()
        return dict(answers=answers, count=all_user_answers)

    def search_question(self, title, limit):
        '''search question by title'''
        self.cursor.execute("SELECT question_id, q_title FROM questions WHERE q_title = (%s);", (title,))
        result = self.cursor.fetchone()
        if result:
            return self.get_single_question(result[0])
        self.cursor.execute("SELECT q_title FROM questions")
        result = self.cursor.fetchmany(limit)
        flattened_list = list(chain.from_iterable(result))
        search_result = get_close_matches(title, flattened_list, n=15)
        self.conn.close()
        return dict(response=search_result, status_code=200)
