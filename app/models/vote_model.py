'''app/models/vote_model.py'''
from app.models.base_models import BaseModel

class VoteModel(BaseModel):
    '''class representing voting model'''
    def upvote(self, my_list):
        '''upvote'''
        user_vote, upvotes, downvotes, answer_id, username = my_list[0], my_list[1], my_list[2], my_list[3], my_list[4]
        if user_vote == 1:
            return dict(response=dict(message="Upvote already noted.", upvotes=upvotes, downvotes=downvotes), status_code=200)
        if user_vote == -1:
            downvotes = downvotes - 1
            self.cursor.execute("UPDATE answers SET downvotes = (%s) WHERE answer_id = (%s);", (downvotes, answer_id,))
            self.cursor.execute("UPDATE votes SET vote = (%s) WHERE v_username = (%s);", (1, username,))
        if user_vote == 0:
            self.cursor.execute("INSERT INTO votes (a_id, v_username, vote) VALUES(%s, %s, %s);", (answer_id, username, 1))
        upvotes = upvotes + 1
        self.cursor.execute("UPDATE answers SET upvotes = (%s) WHERE answer_id = (%s);", (upvotes, answer_id,))
        return dict(votes=dict(upvotes=upvotes, downvotes=downvotes))

    def downvote(self, user_vote, upvotes, downvotes, answer_id, username):
        '''downvote'''
        if user_vote == -1:
            return dict(response=dict(message="Downvote already noted.", upvotes=upvotes, downvotes=downvotes), status_code=200)
        if user_vote == 1:
            upvotes = upvotes - 1
            self.cursor.execute("UPDATE answers SET upvotes = (%s) WHERE answer_id = (%s);", (upvotes, answer_id,))
            self.cursor.execute("UPDATE votes SET vote = (%s) WHERE v_username = (%s);", (-1, username,))
        if user_vote == 0:
            self.cursor.execute("INSERT INTO votes (a_id, v_username, vote) VALUES(%s, %s, %s);", (answer_id, username, -1))
        downvotes = downvotes + 1
        self.cursor.execute("UPDATE answers SET downvotes = (%s) WHERE answer_id = (%s);", (downvotes, answer_id,))
        return dict(votes=dict(upvotes=upvotes, downvotes=downvotes))

    def upvote_or_downvote(self, question_id, answer_id, username, vote):
        '''upvote or downvote an answer'''
        result = self.check_if_question_exists(question_id)
        if isinstance(result, bool):
            result = self.check_if_answer_exists(answer_id)
            if not isinstance(result, dict):    
                if username == result[3]:
                    self.conn.close()
                    return dict(response=dict(message="You cannot vote on your own answer."), status_code=401)
                self.cursor.execute("SELECT vote FROM votes WHERE v_username = (%s) AND a_id = (%s)", (username, answer_id,))
                result = self.cursor.fetchone()
                user_vote = 0
                if result:
                    user_vote = result[0]
                self.cursor.execute("SELECT upvotes FROM answers WHERE answer_id = (%s);", (answer_id,))
                upvotes = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT downvotes FROM answers WHERE answer_id = (%s);", (answer_id,))
                downvotes = self.cursor.fetchone()[0]
                result2 = {}
                if vote == "upvote":
                    result2 = self.upvote([user_vote, upvotes, downvotes, answer_id, username])
                if vote == "downvote":
                    result2 = self.downvote(user_vote, upvotes, downvotes, answer_id, username) 
                if "response" in result2:
                    self.conn.close()
                    return result2
                self.conn.commit()
                result = dict(response=dict(message="Thanks for contributing!", upvotes=result2["votes"]["upvotes"], downvotes=result2["votes"]["downvotes"]), status_code=200)
        self.conn.close()
        return result
