from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'sasquatch_sightings'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash("Name must be at least 2 Characters.", 'register')
            is_valid = False

        if len(results) >= 1:
            flash("Email already exists.", 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", 'register')
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be 8 characters.", 'register')
            is_valid = False

        if user['password'].isalpha() == True or user['password'].islower() == True:
            flash("Password must contain at least 1 number and 1 Uppercase Letter.", 'register')
            is_valid = False

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.", 'register')
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(User.db).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @classmethod
    def get_all_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(User.db).query_db(query, data)
        
        return cls(results[0])

