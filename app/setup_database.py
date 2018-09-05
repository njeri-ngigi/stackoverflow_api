'''app/setup_database.py'''
import psycopg2
from instance.config import app_config

class SetupDB(object):
    '''class to setup db connection'''
    def __init__(self, config_name):
        #create connection to database
        connection_string = app_config[config_name].CONNECTION_STRING
        db_connection = psycopg2.connect(connection_string)
        #create a psycopg2 cursor
        cursor = db_connection.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions(
                question_id   SERIAL PRIMARY KEY,
                q_title       VARCHAR(20)  NOT NULL,
                q_content     VARCHAR(200)  NOT NULL
                );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                user_id    SERIAL PRIMARY KEY,
                name       TEXT         NOT NULL,
                username   VARCHAR(20)  NOT NULL,
                email      VARCHAR(50)  NOT NULL,
                password   VARCHAR(150) NOT NULL
                );''')
        
        db_connection.commit()
        cursor.close()
        db_connection.close()
