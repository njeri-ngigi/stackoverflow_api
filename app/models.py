from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

ALL_USERS = {}
ALL_QUESTIONS = []

class Question():
    def __init__(self, u_title, u_content, u_username):
        self.title = u_title
        self.content = u_content
        self.timestamp = date.today
        self.username = u_username
        self.answers = []
        self.answer_accepted = "none"

    @classmethod
    def getAllQuestions(cls):
        return ALL_QUESTIONS

    @classmethod
    def getSingleQuestion(cls, id):
        if id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        return dict(q=ALL_QUESTIONS[id])

   
class User():
    def __init__(self):
        self.user = {}

    def getAllUsers(self):
        return ALL_USERS

    def addUser(self, name, username, email, password):
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
        if username in ALL_USERS:
            result = check_password_hash(ALL_USERS[username]["password"], password)
            if result:
                return dict(message="Welcome back, " + username + "!")
            return dict(message="Incorrect password", error=401)
        return dict(message="Username doesn't exixt. Try Signing up.", error=401)

    @classmethod
    def postQuestion(cls, title, content, username):
        newQuestion = Question(title, content, username)
        ALL_QUESTIONS.append(newQuestion)
        return dict(title = title)

    @classmethod
    def postAnswer(cls, question_id, username, content):
        if question_id >= len(ALL_QUESTIONS):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        question.answers.append({username:content})
        return dict(message="Answer Posted!")

    @classmethod
    def deleteQuestion(self, id, username):
        if (id >= len(ALL_QUESTIONS)):
            return dict(message="Question doesn't exist", error=404)
        u_question = ALL_QUESTIONS[id]
        if (u_question.username != username):
            return dict(message="Unauthorized to delete this question", error=401)
        ALL_QUESTIONS.pop(id)
        return dict(message="Question " + "#" + str(id) + " Deleted Successfully")

    @classmethod
    def updateAnswer(self, question_id, answer_id, username, content):
        if (question_id >= len(ALL_QUESTIONS)):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        if (answer_id >= len(question.answers)):
            return dict(message="This answer doesn't exist", error=404)
        answer = question.answers[answer_id]
        if username not in answer:
            return dict(message="Unauthorized to edit answer", error=401)
        answer[username] = content
        return dict(message="Answer updated!")

    @classmethod
    def acceptAnswer(self, question_id, answer_id, username):
        if (question_id >= len(ALL_QUESTIONS)):
            return dict(message="Question doesn't exist", error=404)
        question = ALL_QUESTIONS[question_id]
        if username != question.username:
            return dict(message="Unauthorized to accept answer", error=401)
        if (answer_id >= len(question.answers)):
            return dict(message="This answer doesn't exist", error=404)
        question.answer_accepted = answer_id
        return dict(message="Answer #" + str(answer_id) + " accepted!")      
        


    
