from flask_restful import Resource
from flask import request, jsonify

from validate import Validate
from app import User

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return dict(message="Fields cannot be empty"), 400
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not username or not name or not email or not password or not confirm_password:
            return dict(message=
                    "name, username, email, password or confirm_password fields missing"), 400

        u_valid = Validate()
        result = u_valid.validate_register(username, name, email, password, confirm_password)

        if "message" in result:
            return result, 400

        my_user = User()
        result = my_user.addUser(name, username, email, password)
        if result["message"] == "Username already exists. Try a different one.":
            return result, 409
        return result, 201
