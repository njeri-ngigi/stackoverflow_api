'''instance/config.py'''
class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = 'HACHoooaadsf8960-38-(*&^W(*kdfll'
    
class DevelopmentConfig(Config):
    '''Configurations for development'''
    Debug = True

class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    Debug = True
    
app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig
}
