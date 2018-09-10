'''app/application.py'''
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from instance.config import app_config
from app.setup_database import SetupDB

def create_app(config_name):
    '''function enclosing the Flask App'''
    os.environ["ENV"] = config_name
    from app.views import (Signup, Login, Logout, 
                           Questions, QuestionsQuestionId, QuestionsAnswers, QuestionsAnswersId)
    from app.models.revoked_token_model import RevokedTokens
    
    SetupDB(config_name)

    app = Flask(__name__)
    api = Api(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config["TESTING"] = True

    app.config['JWT_SECRET_KEY'] = 'ifv2384834-9jkdvhbvdf023!'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def _check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in BLACKLIST'''
        json_token_identifier = decrypted_token['jti']
        revoked_tokens = RevokedTokens()
        return revoked_tokens.is_jti_blacklisted(json_token_identifier)

    #Add resources to routes
    api.add_resource(Signup, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Logout, '/api/v1/auth/logout')
    api.add_resource(Questions, '/api/v1/questions')
    api.add_resource(QuestionsQuestionId, '/api/v1/questions/<question_id>')
    api.add_resource(QuestionsAnswers, '/api/v1/questions/<question_id>/answers')
    api.add_resource(QuestionsAnswersId, '/api/v1/questions/<question_id>/answers/<answer_id>')
    return app

# Find out how too set environment name during runtime and retrieve it at runtimelike using os.get() something
