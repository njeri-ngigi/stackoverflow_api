'''views/user_registration.py'''
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)

from app.views.validate import Validate
from app.models.user_model import User
from app.models.revoked_token_model import RevokedTokens

class Signup(Resource):
    '''Class representing user registration'''
    @classmethod
    def post(cls):
        '''post (signup method)'''
        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty"), 400
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not username or not name or not email or not password or not confirm_password:
            return dict(
                message="name, username, email, password or confirm_password fields missing"), 400
        u_valid = Validate()
        result = u_valid.validate_register(username, name, email, password, confirm_password)

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
        if not data:
            return dict(message="Please enter username and password"), 400
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return dict(message="Username or password fields missing")
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
        