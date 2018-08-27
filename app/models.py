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

    @classmethod
    def getAllQuestions(cls):
        return ALL_QUESTIONS

    @classmethod
    def getSingleQuestion(cls, id):
        return ALL_QUESTIONS[id]
   
class User():
    def __init__(self):
        self.user = {}

    def getAllUsers(self):
        return ALL_USERS

    def addUser(self, name, username, email, password):
        if username in ALL_USERS:
            return dict(message="Username already exists. Try a different one.")
        self.user["name"] = name
        self.user["email"] = email
        pw_hash = generate_password_hash(password)
        self.user["password"] = pw_hash

        ALL_USERS[username] = self.user

        return dict(message="Welcome " + username + "!")
    
    def login(self, username, password):
        if username in ALL_USERS:
            result = check_password_hash(ALL_USERS[username]["password"], password)
            if result:
                return dict(message="Welcome back, " + username)
            return dict(message="Incorrect password")
        return dict(message="Incorrect username")

    def postQuestion(self, title, content, username):
        newQuestion = Question(title, content, username)
        ALL_QUESTIONS.append(newQuestion)
        return dict(title = content)

    def deleteQuestion(self, id, username):
        if (id > len(ALL_QUESTIONS)):
            return dict(message="Question doesn't exist")
        u_question = ALL_QUESTIONS[id]
        if (u_question.username != username):
            return dict(message="Unauthorized to delete this question")
        ALL_QUESTIONS.pop(id)
        return dict(message="Question " + "#" + id + " Deleted Successfully")
