'''views/user_registration.py'''
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)

from app.views.validate import Validate
from app.models.user_model import User
from app.models.revoked_token_model import RevokedTokens

validate = Validate()

class Signup(Resource):
    '''Class representing user registration'''
    @classmethod
    def post(cls):
        '''post (signup method)'''
        data = request.get_json()
        result = validate.check_for_data(data)
        if result:
            return result, 400
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        message = ""
        if not confirm_password:
            message = "Please Re-enter password"
        if not password:
            message = "Please enter password"
        if not email:
            message = "Please enter email"
        if not username:
            message = "Please enter username"
        if not name:
            message = "Please enter name"
        if message:
            return dict(message=message), 400
        passwords = [password, confirm_password]
        result = validate.validate_register(username, name, email, passwords)
        if "message" in result:
            return result, 400
        my_user = User()
        result = my_user.add_user(name, username, email, password)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        return result, 201

class Login(Resource):
    '''Class representing user login'''
    @classmethod
    def post(cls):
        '''post (login) method'''
        data = request.get_json()
        result = validate.check_for_data(data)
        if result:
            return result, 400
        username = data.get("username")
        password = data.get("password")
        message = ""
        if not password:
            message = "Please enter password"
        if not username:
            message = "Please enter username"
        if message:
            return dict(message=message), 400
        result = validate.check_for_white_spaces([username, password])
        if result:
            return result, 400
        my_user = User()
        result = my_user.login(username, password)
        if "error" in result:
            return dict(message=result["message"]), result["error"]
        access_token = create_access_token(identity=username)
        return dict(result, token=access_token), 200

class Logout(Resource):
    ''' Class representing Logout user by revoking the token given earlier'''
    @classmethod
    @jwt_required
    def post(cls):
        '''post (logout) method'''
        json_token_identifier = get_raw_jwt()['jti']
        revoked_token = RevokedTokens()
        revoked_token.add_token_to_blacklist(json_token_identifier)
        return dict(message="Leaving so soon?"), 200
        