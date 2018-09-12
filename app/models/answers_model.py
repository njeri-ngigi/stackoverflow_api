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
    
    def check_if_answer_exists(self, answer_id):
        'helper method to check if an answer exists'''
        self.cursor.execute("SELECT * FROM answers WHERE answer_id = (%s);", (answer_id,))
        result = self.cursor.fetchone()
        if not result:
            return False
        return result
        
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
        if not a_id:
            self.conn.close()
            return dict(message="Failed to post answer. Try again.", error=404)
        self.cursor.execute("SELECT q_answers FROM questions WHERE question_id = (%s);",(question_id,))
        q_answers = self.cursor.fetchone()[0]
        q_answers = q_answers + 1
        self.cursor.execute("UPDATE questions SET q_answers = (%s) WHERE question_id = (%s);", (q_answers, question_id,))
        self.conn.commit()
        self.conn.close()
        return dict(message="Answer Posted!")

    def get_all_answers_to_question(self, question_id, limit=None):
        '''get all answers to a question'''
        result = self.check_if_question_exists(question_id)
        if not result:
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
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        result2 = self.check_if_answer_exists(answer_id)
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

    def upvote_or_downvote(self, question_id, answer_id, username, vote):
        '''upvote or downvote an answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        result2 = self.check_if_answer_exists(answer_id)
        if not result2:
            self.conn.close()
            return dict(message="This answer doesn't exist", error=404)
        if username == result2[3]:
            self.conn.close()
            return dict(message="You cannot vote on your own answer.", error=401)
        self.cursor.execute("SELECT vote FROM votes WHERE v_username = (%s)",(username,))
        result4 = self.cursor.fetchone()
        user_vote = 0
        if result4:
            user_vote = result4[0]
        self.cursor.execute("SELECT upvotes FROM answers WHERE answer_id = (%s);", (answer_id,))
        upvotes = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT downvotes FROM answers WHERE answer_id = (%s);", (answer_id,))
        downvotes = self.cursor.fetchone()[0]
        if vote == "upvote":
            if user_vote == 1:
                return dict(message="Upvote already noted.")
            if user_vote == -1:
                downvotes = downvotes - 1
                self.cursor.execute("UPDATE answers SET downvotes = (%s) WHERE answer_id = (%s);", (downvotes, answer_id,))
                self.cursor.execute("UPDATE votes SET vote = (%s) WHERE v_username = (%s);", (1, username,))
            upvotes = upvotes + 1
            self.cursor.execute("UPDATE answers SET upvotes = (%s) WHERE answer_id = (%s);", (upvotes, answer_id,))
            if user_vote == 0:
                self.cursor.execute("INSERT INTO votes (a_id, v_username, vote) VALUES(%s, %s, %s);", (answer_id, username, 1))
        if vote == "downvote":
            if user_vote == -1:
                return dict(message="Downvote already noted.")
            if user_vote == 1:
                upvotes = upvotes - 1
                self.cursor.execute("UPDATE answers SET upvotes = (%s) WHERE answer_id = (%s);", (upvotes, answer_id,))
                self.cursor.execute("UPDATE votes SET vote = (%s) WHERE v_username = (%s);", (-1, username,))
            downvotes = downvotes + 1
            self.cursor.execute("UPDATE answers SET downvotes = (%s) WHERE answer_id = (%s);", (downvotes, answer_id,))
            if user_vote == 0:
                self.cursor.execute("INSERT INTO votes (a_id, v_username, vote) VALUES(%s, %s, %s);", (answer_id, username, -1))
        self.conn.commit()
        self.conn.close()
        return dict(message="Thanks for contributing!")

    def post_comment(self, question_id, answer_id, username, content):
        '''post comment on answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        result = self.check_if_answer_exists(answer_id)
        if not result:
            self.conn.close()
            return dict(message="This answer doesn't exist", error=404)
        self.cursor.execute("SELECT * FROM comments WHERE c_username = (%s) AND c_content = (%s);", (username, content,))
        result2 = self.cursor.fetchone()
        if result2:
            self.conn.close()
            return dict(message="Comment already noted. To edit comment visit question #" +
                        str(question_id) + " answer #" + str(answer_id) + " comment #" + str(result2[0]),
                        question_id=question_id, answer_id=answer_id, comment_id=result2[0], error=409)
        sql = "INSERT INTO comments (a_id, c_username, c_content) VALUES (%s, %s, %s);"
        self.cursor.execute(sql, (answer_id, username, content))
        comments = result[7]
        comments = comments + 1
        self.cursor.execute("UPDATE answers SET comments = (%s) WHERE answer_id = (%s);", (comments, answer_id))
        self.conn.commit()
        self.conn.close()
        return dict(message="Comment posted!")

    def get_answer_comments(self, question_id, answer_id, limit=None):
        '''get all comments for an answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        result = self.check_if_answer_exists(answer_id)
        if not result:
            self.conn.close()
            return dict(message="This answer doesn't exist", error=404)
        self.cursor.execute("SELECT * FROM comments WHERE a_id = (%s);", (answer_id,)) 
        if limit:
            result2 = self.cursor.fetchmany(limit)
            self.conn.close()
            return result2
        result2 = self.cursor.fetchall()
        self.conn.close()
        return result2

    def update_comment(self, question_id, answer_id, comment_id, username, content):
        '''update a comment on an answer'''
        result = self.check_if_question_exists(question_id)
        if not result:
            self.conn.close()
            return dict(message="Question doesn't exist", error=404)
        result = self.check_if_answer_exists(answer_id)
        if not result:
            self.conn.close()
            return dict(message="This answer doesn't exist", error=404)
        self.cursor.execute("SELECT c_username FROM comments WHERE comment_id = (%s);", (comment_id,)) 
        result = self.cursor.fetchone()
        if not result:
            self.conn.close()
            return dict(message="Comment doesn't exist", error=404)
        if result[0] != username:
            self.conn.close()
            return dict(message="Unauthorized to edit this comment.", error=401)
        self.cursor.execute("UPDATE comments SET c_content = (%s) WHERE comment_id = (%s);", (content, comment_id))
        self.conn.commit()
        self.conn.close()
        return dict(message="Comment updated!")
