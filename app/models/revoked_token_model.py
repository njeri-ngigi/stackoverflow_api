'''app/models/revoked_token_model.py'''
import psycopg2
from app.models.base_models import BaseModel

class RevokedTokens(BaseModel):
    '''class representing revoked tokens model'''
    def add_token_to_blacklist(self, json_token_identifier):
        '''add token to blacklist'''
        sql = "INSERT INTO revoked_tokens (json_token_identifier) VALUES (%s);"
        self.cursor.execute(sql, (json_token_identifier,))
        self.conn.commit()
        self.conn.close()

    def is_jti_blacklisted(self, json_token_identifier):
        '''check if token is blacklisted'''
        self.cursor.execute("select * from revoked_tokens where json_token_identifier = (%s);", (json_token_identifier,))
        result = bool(self.cursor.fetchone())
        self.conn.close()
        return result
