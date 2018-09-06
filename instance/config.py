'''instance/config.py'''

class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = 'Sqklpeikvnjn!^Tghbvq8wij90!'
    CONNECTION_STRING = "dbname='db_stackoverflow_lite' user='postgres' host='localhost' password='testme'"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testme@localhost:5432/db_stackoverflow_lite'

class DevelopmentConfig(Config):
    '''configurations for development'''
    DEBUG = True

class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    DEBUG = True
    CONNECTION_STRING = "dbname='test_db' user='postgres' host='localhost' password='testme'"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testme@localhost/test_db'

class ProductionConfig(Config):
    '''configurations for production'''
    DEBUG = False
    TESTING = False

app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production': ProductionConfig
}
