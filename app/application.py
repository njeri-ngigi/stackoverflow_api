from flask import Flask
from flask_restful import Api

from instance import app_config

def createApp(config_name):
    '''function enclosing the Flask App'''
    from views import Signup

    app = Flask(__name__)
    api = Api(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config["TESTING"] = True
    app.config['JWT_SECRET_KEY'] = 'my-key'
    
    api.add_resource(Signup, '/api/v1/auth/signup')

    return app
