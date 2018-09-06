'''revoked_token_model.py'''
import os
import psycopg2
from instance.config import app_config

CURRENT_ENVIRONMENT = os.environ['ENV']
CONN_STRING = app_config[CURRENT_ENVIRONMENT].CONNECTION_STRING

class RevokedTokens(object):
    def __init__(self):
        '''set up class variables'''
        self.conn = psycopg2.connect(CONN_STRING)
        self.cursor = self.conn.cursor()

    def add_token_to_blacklist(self, json_token_identifier):
        sql = "INSERT INTO revoked_tokens (json_token_identifier) VALUES (%s);"
        self.cursor.execute(sql,(json_token_identifier,))
        self.conn.commit()
        self.conn.close()

    def is_jti_blacklisted(self, json_token_identifier):
        '''check if token is blacklisted'''
        self.cursor.execute("select * from revoked_tokens where json_token_identifier = (%s);", (json_token_identifier,))   
        result = bool(self.cursor.fetchone())
        self.conn.close()
        return result
