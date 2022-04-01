from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt =  Bcrypt(app)

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def createuser(cls, data):
        hashed_pass = bcrypt.generate_password_hash(data["password"])
        user = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hashed_pass
        }
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) " \
            "VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW());"
        return connectToMySQL('exam_schema').query_db(query, user)
    
    @classmethod
    def all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('exam_schema').query_db(query)
        users = []
        for item in results:
            users.append(cls(item))
        return users

    # this is used for later on to validate email
    @classmethod
    def user_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        if results:
            return cls(results[0]) 
        return False


    # use this to start user session and to pull info to the seesion
    @classmethod
    def user_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        if results:
            return cls(results[0]) 
        return False
    
    # pulls user_email and bcrypyt to check password
    @classmethod
    def validate_login(cls, data):
        user_validated = User.user_email(data)
        if not user_validated:
            flash("Invalid Email or Password","login")
            return False
        if not bcrypt.check_password_hash(user_validated.password, data["password"]):
            flash("Invalid Email or Password","login")
            return False
        return True

    #use this to check if email is already in sql
    @staticmethod
    def email_is_valid(email):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('exam_schema').query_db(query,email)
        if results:
            flash("Email is Already In Use","register")
            is_valid=False
        return is_valid


    # use this in the register form for validating each input
    @staticmethod
    def validate_register_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First Name must be 2 characters or longer.","register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last Name must be 2 characters or longer.","register")
            is_valid = False
        #use regex to confirm if email has @ sign
        if not EMAIL_REGEX.match(data['email']):
            flash("Email address is not usable","register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters.","register")
            is_valid = False
        # validates if passwords and confirm are same
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Confrim Password does not match","register")
        return is_valid
    
