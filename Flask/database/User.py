import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_user(cls, username, password):
        connection = sqlite3.connect(r"E:\Long\Web\Flask\database\data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        result = cursor.execute(query, (username, password))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
