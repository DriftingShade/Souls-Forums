from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")


class User:
    DB = "souls_db"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.threads = []

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user["first_name"].strip()) == 0:
            flash("First Name is required", "register")
            is_valid = False
        elif len(user["first_name"].strip()) < 3:
            flash("First Name must be at least 2 characters", "register")
            is_valid = False

        if len(user["last_name"].strip()) == 0:
            flash("Last Name is required", "register")
            is_valid = False
        elif len(user["last_name"].strip()) < 3:
            flash("Last Name must be at least 2 characters", "register")
            is_valid = False

        if len(user["username"].strip()) == 0:
            flash("Username is required", "register")
            is_valid = False
        elif len(user["username"].strip()) < 3:
            flash("Username must be at least 3 characters", "register")
            is_valid = False
        elif len(user["username"].strip()) > 15:
            flash("Username must be less than 15 characters", "register")
            is_valid = False

        if len(user["email"].strip()) == 0:
            flash("Email Address is required", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address", "register")
            is_valid = False

        if len(user["password"].strip()) == 0:
            flash("Please enter password.", "register")
            is_valid = False
        elif len(user["password"].strip()) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        elif not PASSWORD_REGEX.match(user["password"].strip()):
            flash(
                "Password must contain at least 1 capital letter, 1 number and 1 special character (!@#$)",
                "register",
            )
            is_valid = False
        elif user["password"] != user["password_confirm"]:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user["email"].strip()) == 0:
            flash("Email Address is required", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address", "login")
            is_valid = False

        if len(user["password"].strip()) == 0:
            flash("Please enter password.", "login")
            is_valid = False
        elif len(user["password"].strip()) < 8:
            flash("Password must be at least 8 characters", "login")
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, data):
        query = """INSERT INTO users (first_name, last_name, username, email, password, 
        created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(username)s, %(email)s, 
        %(password)s, NOW(), NOW());"""

        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results

    @classmethod
    def find_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return None
        user = User(results[0])
        return user

    @classmethod
    def find_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {"user_id": user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return None
        user = User(results[0])
        return user

    @classmethod
    def find_by_id_with_threads(cls, user_id):
        query = """SELECT * FROM users LEFT JOIN threads ON users.id = 
        threads.user_id WHERE users.id = %(user_id)s"""
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        user = User(list_of_dicts[0])
        for each_dict in list_of_dicts:
            if each_dict["threads.id"] != None:
                thread_data = {
                    "id": each_dict["threads.id"],
                    "title": each_dict["title"],
                    "content": each_dict["content"],
                    "created_at": each_dict["threads.created_at"],
                    "updated_at": each_dict["threads.updated_at"],
                    "user_id": each_dict["user_id"],
                }
                thread = thread.Thread(thread_data)
                user.threads.append(thread)

        return user