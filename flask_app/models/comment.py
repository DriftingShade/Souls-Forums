from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.thread import Thread
from pprint import pprint


class Comment:
    DB = "souls_db"

    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.thread_id = data["thread_id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = {
            "id": data["users.id"],
            "username": data["username"],
        }

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        if len(form_data["content"]) == 0:
            flash("Please enter a comment.")
            is_valid = False
        elif len(form_data["content"]) < 3:
            flash("Comment must be at least three characters.")
            is_valid = False

        return is_valid

    @classmethod
    def all_comments(cls, thread_id):
        data = {"thread_id": thread_id}
        query = """SELECT *
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.thread_id = %(thread_id)s
                ORDER BY comments.created_at DESC; """
        list_of_dicts = connectToMySQL(Comment.DB).query_db(query, data)
        pprint(list_of_dicts)

        comments = []
        for each_dict in list_of_dicts:
            comment = Comment(each_dict)
            comments.append(comment)
        return comments

    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO comments (user_id, thread_id, content) 
        VALUES (%(user_id)s, %(thread_id)s, %(content)s);"""
        connectToMySQL(Comment.DB).query_db(query, form_data)
        return

    @classmethod
    def delete_comment(cls, comment_id):
        query = """DELETE FROM comments WHERE id = %(comment_id)s"""
        data = {"comment_id": comment_id}
        connectToMySQL(Comment.DB).query_db(query, data)
        return