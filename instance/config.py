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
    SECRET_KEY = 'KjkhFDjihkgy#$&(hdsdsddR#$gdd!'

class ProductionConfig(Config):
    '''configurations for production'''
    DEBUG = False
    TESTING = False
    CONNECTION_STRING = 'postgres://lgltqihiazvjfw:10428ba23af1a311d539ab7a0f99f00c1efa2bbb34841b8bfad5d47d73df90e9@ec2-75-101-153-56.compute-1.amazonaws.com:5432/d3ruee63uidar1'

app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production': ProductionConfig
}
