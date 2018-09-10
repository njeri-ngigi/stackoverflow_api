'''app/models.user_model.py'''
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class User(object):
    '''User class model'''
    def __init__(self):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def add_user(self, name, username, email, password):
        '''Add a user'''
        pw_hash = generate_password_hash(password)
        # check if username already exists
        self.cursor.execute("select * from users where username = (%s);", (username,))
        result = self.cursor.fetchone()
        if result:
            self.conn.close()
            return dict(message="Username already exists. Try a different one.", error=409)
        self.cursor.execute("select * from users where email = (%s);", (email,))
        result2 = self.cursor.fetchone()
        if result2:
            return dict(message="Email already in use. Try a different one.", error=409)
       
        sql = """INSERT INTO users(name, username, email, password)
                 VALUES(%s, %s, %s, %s);"""
        self.cursor.execute(sql, (name, username, email, pw_hash))
        self.conn.commit()
        # check that user was signed up
        self.cursor.execute("select * from users where username = (%s);", (username,))
        result2 = self.cursor.fetchone()
        self.conn.close()
        if not result2:
            return dict(message="Failed to signup, try again.", error=404)
        return dict(message="Welcome " + username + "!")
        

    def login(self, username, password):
        '''login user'''
        self.cursor.execute("SELECT username, password FROM users WHERE username = (%s);", (username,))
        result = self.cursor.fetchone()
        self.conn.close()
        if not result:
            return dict(message="Username doesn't exixt. Try Signing up.", error=401)
        is_password_correct = check_password_hash(result[1], password)
        if is_password_correct:
            return dict(message="Welcome back, " + username + "!")
        return dict(message="Incorrect password", error=401)
