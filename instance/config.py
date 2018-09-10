'''instance/config.py'''
import os

class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')

class DevelopmentConfig(Config):
    '''configurations for development'''
    DEBUG = True

class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    DEBUG = True
    CONNECTION_STRING = "dbname='test_db' user='postgres' host='localhost' password='testme'"
    
class ProductionConfig(Config):
    '''configurations for production'''
    DEBUG = False
    TESTING = False

app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production': ProductionConfig
}
