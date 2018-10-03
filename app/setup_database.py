'''app/setup_database.py'''
import psycopg2
from instance.config import app_config

class SetupDB(object):
    '''class to setup db connection'''
    def __init__(self, config_name):
        #create connection to database
        connection_string = app_config[config_name].CONNECTION_STRING
        self.db_connection = psycopg2.connect(connection_string)
        #create a psycopg2 cursor
        self.cursor = self.db_connection.cursor()

    def create_db(self):
        '''method creating tables'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions(
                question_id          SERIAL PRIMARY KEY,
                q_title              VARCHAR(50)  NOT NULL,
                q_content            VARCHAR(200)  NOT NULL,
                q_username           VARCHAR(20) NOT NULL,
                q_accepted_answer    INTEGER DEFAULT 0,
                q_answers            INTEGER DEFAULT 0
                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                user_id    SERIAL PRIMARY KEY,
                name       TEXT         NOT NULL,
                username   VARCHAR(20)  UNIQUE NOT NULL,
                email      VARCHAR(50)  UNIQUE NOT NULL,
                password   VARCHAR(150) NOT NULL
                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS revoked_tokens(
                token_id                SERIAL PRIMARY KEY,
                json_token_identifier   VARCHAR(200)
                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers(
                answer_id     SERIAL UNIQUE NOT NULL,
                q_id          INTEGER REFERENCES questions(question_id) ON DELETE CASCADE,
                a_content     VARCHAR(200) NOT NULL,
                a_username    VARCHAR(20) NOT NULL,
                accepted      INTEGER DEFAULT 0,
                upvotes       INTEGER DEFAULT 0,
                downvotes     INTEGER DEFAULT 0,
                comments      INTEGER DEFAULT 0,
                PRIMARY KEY   (answer_id, q_id)
                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS votes(
                vote_id       SERIAL UNIQUE NOT NULL,
                a_id          INTEGER REFERENCES answers(answer_id) ON DELETE CASCADE,
                v_username    VARCHAR(20) NOT NULL,
                vote          INTEGER DEFAULT 0,
                PRIMARY KEY   (vote_id, a_id)
                );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                comment_id    SERIAL UNIQUE NOT NULL,
                a_id          INTEGER REFERENCES answers(answer_id) ON DELETE CASCADE,
                c_username    VARCHAR(20) NOT NULL,
                c_content     VARCHAR(200) NOT NULL,
                PRIMARY KEY   (comment_id, a_id)
                );''')
        self.db_connection.commit()
        self.cursor.close()
        self.db_connection.close()
    