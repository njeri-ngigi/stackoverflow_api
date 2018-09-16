'''app/models/answers_model.py'''
import psycopg2
from app.models.base_models import BaseModel

class AnswersModel(BaseModel):
    '''answers class model'''
    def post_answer(self, question_id, content, username):
        '''post an answer'''
        result = self.check_if_question_exists(question_id)
        if type(result) != bool:
            self.conn.close()
            return dict(response=dict(message="Question doesn't exist"), status_code=404)
        self.cursor.execute('''SELECT answer_id, a_username FROM answers
                            WHERE a_content = (%s);''', (content, ))
        result = self.cursor.fetchone()
        if result:
            if result[1] == username:
                self.conn.close()
                return dict(response=dict(message="You have already posted this answer. To edit answer vist question #"
                            + str(question_id) + " answer #" + str(result[0]),
                            question_id=question_id, answer_id=result[0]), status_code=409)
        sql = "INSERT INTO answers (q_id, a_content, a_username) VALUES (%s, %s, %s) RETURNING answer_id;"
        self.cursor.execute(sql, (question_id, content, username))
        a_id = self.cursor.fetchone()[0]
        if not a_id:
            self.conn.close()
            return dict(response=dict(message="Failed to post answer. Try again."), status_code=500)
        self.cursor.execute("SELECT q_answers FROM questions WHERE question_id = (%s);", (question_id,))
        q_answers = self.cursor.fetchone()[0]
        q_answers = q_answers + 1
        self.cursor.execute("UPDATE questions SET q_answers = (%s) WHERE question_id = (%s);",
                            (q_answers, question_id,))
        self.conn.commit()
        self.conn.close()
        return dict(response=dict(message="Answer Posted!"), status_code=201)

    def get_all_answers_to_question(self, question_id, limit=None):
        '''get all answers to a question'''
        result = self.check_if_question_exists(question_id)
        if type(result) != bool:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        self.cursor.execute("SELECT * FROM answers WHERE q_id = (%s) ORDER BY accepted DESC;", (question_id,))
        if limit:
            result2 = self.cursor.fetchmany(limit)
            self.conn.close()
            return result2
        result2 = self.cursor.fetchall()
        self.conn.close()
        return result2

    def update_or_accept_answer(self, question_id, answer_id, username, content, action):
        '''Update or accept answer'''
        result = self.check_if_question_exists(question_id)
        if type(result) == bool:
            result = self.check_if_answer_exists(answer_id)
            if type(result) != dict:
                if action == "update":
                    if username == result[3]:
                        self.cursor.execute("UPDATE answers SET a_content = (%s) WHERE answer_id = (%s);",
                                            (content, answer_id,))
                        self.conn.commit()
                        result = dict(response=dict(message="Answer updated!"), status_code=200)
                    else:
                        result = (dict(response=dict(message="Unauthorized to edit answer"), status_code=401))
                if action == "accept":
                    self.cursor.execute("SELECT q_username FROM questions WHERE question_id = (%s);", (question_id,))
                    u_name = self.cursor.fetchone()[0]
                    if username == u_name:
                        sql = "UPDATE answers SET accepted = (%s) WHERE"
                        self.cursor.execute(sql + " accepted = (%s);", (0, 1,))
                        self.cursor.execute(sql + " answer_id = (%s);", (1, answer_id,))
                        self.cursor.execute("UPDATE questions SET q_accepted_answer = (%s) WHERE question_id = (%s);", (answer_id, question_id,))
                        self.conn.commit()
                        result = dict(response=dict(message="Answer #" + str(answer_id) + " accepted!"), status_code=200)
                    else:
                        result = dict(response=dict(message="Unauthorized to accept answer"), status_code=401)
        self.conn.close()
        return result

    def post_comment(self, question_id, answer_id, username, content):
        '''post comment on answer'''
        result = self.check_if_question_exists(question_id)
        if type(result) == bool:
            result = self.check_if_answer_exists(answer_id)
            if type(result) != dict:
                self.cursor.execute("SELECT * FROM comments WHERE c_username = (%s) AND c_content = (%s);", (username, content,))
                result2 = self.cursor.fetchone()
                if result2:
                    result = dict(response=dict(message="Comment already noted. To edit comment visit question #" +
                    str(question_id) + " answer #" + str(answer_id) + " comment #" + str(result2[0]),
                    question_id=question_id, answer_id=answer_id, comment_id=result2[0]), status_code=409)
                else:
                    sql = "INSERT INTO comments (a_id, c_username, c_content) VALUES (%s, %s, %s);"
                    self.cursor.execute(sql, (answer_id, username, content,))
                    comments = result[7]
                    comments = comments + 1
                    self.cursor.execute("UPDATE answers SET comments = (%s) WHERE answer_id = (%s);", (comments, answer_id))
                    self.conn.commit()
                    result = dict(response=dict(message="Comment posted!"), status_code=201)
        self.conn.close()
        return result
    def get_answer_comments(self, question_id, answer_id, limit=None):
        '''get all comments for an answer'''
        result = self.check_if_question_exists(question_id)
        if type(result) == bool:
            result = self.check_if_answer_exists(answer_id)
            if type(result) != dict:
                self.cursor.execute("SELECT * FROM comments WHERE a_id = (%s);", (answer_id,))
                if limit:
                    result2 = self.cursor.fetchmany(limit)
                else:
                    result2 = self.cursor.fetchall()
                self.conn.close()
                return result2
        self.conn.close()
        return result

    def update_comment(self, question_id, answer_id, comment_id, username, content):
        '''update a comment on an answer'''
        result = self.check_if_question_exists(question_id)
        if type(result) == bool:
            result = self.check_if_answer_exists(answer_id)
            if type(result) != dict:
                self.cursor.execute("SELECT c_username FROM comments WHERE comment_id = (%s);", (comment_id,))
                result = self.cursor.fetchone()
                if not result:
                    result = dict(response=dict(message="Comment doesn't exist"), status_code=404)              
                else:
                    if result[0] == username:
                        self.cursor.execute("UPDATE comments SET c_content = (%s) WHERE comment_id = (%s);", (content, comment_id))
                        self.conn.commit()
                        result = dict(response=dict(message="Comment updated!"), status_code=200)
                    else:
                        result = dict(response=dict(message="Unauthorized to edit this comment."), status_code=401)       
        self.conn.close()
        return result
