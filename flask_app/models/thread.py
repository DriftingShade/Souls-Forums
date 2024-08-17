from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Thread:
    DB = "souls_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        if len(form_data["title"].strip()) == 0:
            flash("Please enter title.")
            is_valid = False
        elif len(form_data["title"].strip()) < 5:
            flash("Title must be at least five characters.")
            is_valid = False
        elif len(form_data["title"].strip()) > 60:
            flash("Title must be less than 60 characters.")
            is_valid = False

        if len(form_data["content"].strip()) == 0:
            flash("Please enter content.")
            is_valid = False
        elif len(form_data["content"].strip()) < 10:
            flash("Content must be at least 10 characters.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        query = """SELECT * FROM threads JOIN users ON threads.user_id = users.id"""
        list_of_dicts = connectToMySQL(Thread.DB).query_db(query)

        threads = []
        for each_dict in list_of_dicts:
            thread = Thread(each_dict)
            threads.append(thread)
        return threads

    @classmethod
    def find_all_with_users(cls):
        query = """SELECT * FROM threads JOIN users ON threads.user_id = users.id"""

        list_of_dicts = connectToMySQL(Thread.DB).query_db(query)

        threads = []
        for each_dict in list_of_dicts:
            thread = Thread(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "username": each_dict["username"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = User(user_data)
            thread.user = user
            threads.append(thread)
        return threads

    @classmethod
    def find_by_id(cls, thread_id):
        query = """SELECT * FROM threads WHERE id = %(thread_id)s"""
        data = {"thread_id": thread_id}
        list_of_dicts = connectToMySQL(Thread.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        thread = Thread(list_of_dicts[0])
        return thread

    @classmethod
    def find_by_id_with_user(cls, thread_id):
        query = """SELECT * FROM threads JOIN users ON threads.user_id = users.id 
        WHERE threads.id = %(thread_id)s"""

        data = {"thread_id": thread_id}
        list_of_dicts = connectToMySQL(Thread.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        thread = Thread(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "username": list_of_dicts[0]["username"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        thread.user = User(user_data)
        return thread

    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO threads
        (title, content, user_id, created_at, updated_at)
        VALUES
        (%(title)s, %(content)s, %(user_id)s, NOW(), NOW());"""
        thread_id = connectToMySQL(Thread.DB).query_db(query, form_data)
        return thread_id

    @classmethod
    def update(cls, form_data):
        query = """UPDATE threads
        SET
        title=%(title)s,
        content=%(content)s,
        user_id=%(user_id)s,
        updated_at=NOW()
        WHERE id = %(thread_id)s;"""
        connectToMySQL(Thread.DB).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, thread_id):
        query = """DELETE FROM threads WHERE id = %(thread_id)s;"""
        data = {"thread_id": thread_id}
        connectToMySQL(Thread.DB).query_db(query, data)
        return
