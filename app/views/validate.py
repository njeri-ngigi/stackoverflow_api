'''views/validate.py'''
import re

class Validate(object):
    '''Helper class for input validation'''
    def __init__(self):
        self.special_character_regex = r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'

    @classmethod
    def validate_email(cls, email):
        '''validating email format'''
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return dict(message="Enter a valid email address")
        return email

    def validate_password(self, password, confirm_password):
        '''method checking pasword requirements'''
        error = {}
        if confirm_password != password:
            error["message"] = "Passwords don't match"
        if bool(re.search(r'[A-Z][a-z]|[a-z][A-Z]', password)) is False:
            error["message"] = "password must contain a mix of upper and lowercase letters"
        if bool(re.search(self.special_character_regex, password)) is False:
            error["message"] = "password must contain atleast one numeric or special character"
        if len(password) < 6:
            error["message"] = "password is too short. Minimum length is 6 characters."
        if "message" in error:
            return error
        return password

    def validate_username(self, username):
        #search for only numbers and special characters
        if len(username) < 4:
            return {"message": "Username should be 4 or more characters"}
        if len(username) > 29:
            return {"message": "Username is too long. Try one between 4 & 29 characters"}
        if username.isdigit():
            return {"message": "Username cannot contain only numbers"}
        if bool(re.search(r'[^a-zA-Z0-9_]', username)):
            return {"message": "Username cannot contain special characters"}
        return username

    def validate_name(self, name):
        '''method to check for special characters in name'''
        if bool(re.search(self.special_character_regex, name)) is True:
            return {"message":"Name cannot contain special characters and numbers"}
        if len(name) < 4:
            return {"message":"Name should be 4 or more characters"}
        return name

    def check_for_white_spaces(self, my_list):
        '''method checking for whitespaces'''
        for i in my_list:
            i = i.strip()
            if not i:
                return {"message": "Enter valid data. Look out for whitespaces in field(s)."}

    def check_for_data(self, data):
        '''method checking for data'''
        if not data:
            return dict(message="Field(s) cannot be empty")

    def check_for_length(self, title):
        '''method checking for length of title'''
        if len(title) > 49:
            return dict(message="Title is too long. Please shorten it.")

    def check_for_content(self, content):
        '''checking for content'''
        message = ""
        message = "Please enter content"
        if len(content) > 1:
            if not content[0]:
                message = "Please enter title"
        for i in content:
            if not i:
                return dict(message=message)

    def validate_register(self, username, name, email, passwords):
        '''validate user register data '''
        password = passwords[0]
        confirm_password = passwords[1]
        my_list = [username, name, password]
        result = self.check_for_white_spaces(my_list)
        email = self.validate_email(email)
        password = self.validate_password(password, confirm_password)
        name = self.validate_name(name)
        username = self.validate_username(username)
        my_list2 = [result, name, username, email, password]
        for i in my_list2:
            if isinstance(i, dict):
                if "message" in i:
                    return i
        return {"username":username, "name":name, "password":password, "email":email}
        