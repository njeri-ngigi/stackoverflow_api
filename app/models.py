'''app/models.py'''
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

ALL_USERS = {}
ALL_QUESTIONS = []

class Question(object):
    '''Question class model'''
    def __init__(self, u_title, u_content, u_username):
        '''set up class variables'''
        self.title = u_title
        self.content = u_content
        self.timestamp = date.today
        self.username = u_username
        self.answers = []
        self.answer_accepted = "none"

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
        self.user = {}

    def add_user(self, name, username, email, password):
        '''Add a user'''
        if username in ALL_USERS:
            return dict(message="Username already exists. Try a different one.", error=409)
        self.user["name"] = name
        self.user["email"] = email
        pw_hash = generate_password_hash(password)
        self.user["password"] = pw_hash

        ALL_USERS[username] = self.user

        return dict(message="Welcome " + username + "!")

    @classmethod
    def login(cls, username, password):
        '''login user'''
        if username in ALL_USERS:
            result = check_password_hash(ALL_USERS[username]["password"], password)
            if result:
                return dict(message="Welcome back, " + username + "!")
            return dict(message="Incorrect password", error=401)
        return dict(message="Username doesn't exixt. Try Signing up.", error=401)

    @classmethod
    def post_question(cls, title, content, username):
        '''Post question'''
        for i in ALL_QUESTIONS:
            if i.title == title:
                q_index = ALL_QUESTIONS.index(i)
                return dict(message="Question has already been asked. Vist question #" +
                           str(q_index), question_id=q_index, error=409)
        new_question = Question(title, content, username)
        ALL_QUESTIONS.append(new_question)
        return dict(title=title)

    @classmethod
    def post_answer(cls, question_id, username, content):
        '''Post answer'''
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        for i in question.answers:
            if username == username:
                if i[username] == content:
                    a_index = question.answers.index(i)
                    return dict(message="You have already posted this answer. To edit answer visit question #" + 
                                str(question_id) + " answer #" + str(a_index), question_id=question_id, answer_id=a_index, error=409) 
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
