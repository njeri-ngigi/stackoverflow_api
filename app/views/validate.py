'''validate.py'''
import re
special_character_regex = r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'

class Validate():
    def validate_email(self, email):
        '''validating email format'''
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return dict(message="Enter a valid email address")
        return email

    def validate_password(self, password, confirm_password):
        '''method checking pasword requirements'''
        if len(password) < 6:
            return {"message": "password is too short"}
        if bool(re.search(r'[A-Z][a-z]|[a-z][A-Z]', password)) is False:
            return {"message": "password must contain a mix of upper and lowercase letters"}
        if bool(re.search(special_character_regex, password)) is False:
            return {"message": "password must contain atleast one numeric or special character"}
        if confirm_password != password:
            return {"message": "Passwords don't match"}
        return password
    
    def validate_name(self, name):
        '''method to check for special characters in name'''
        if bool(re.search(special_character_regex, name)) is True:
            return {"message":"Name cannot contain special characters and numbers"}
        return name

    def validate_register(self, username, name, email, password, confirm_password):
        '''validate user register data '''
        my_list = [username, name, password]
        for i in my_list:
            i = i.strip()
            if not i:
                return {"message": "Enter valid data"}
        email = self.validate_email(email)
        password = self.validate_password(password, confirm_password)
        name = self.validate_name(name)
        if "message" in name:
            return name
        if "message" in email:
            return email
        if "message" in password:
            return password
        
        return {"username":username, "name":name, "password":password, "email":email}
        