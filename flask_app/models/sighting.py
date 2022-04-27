from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from datetime import datetime

class Sighting:
    db = 'sasquatch_sightings'
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date = data['date']
        self.num_of_sasquatch = data['num_of_sasquatch']
        self.user_id = user.User.get_all_by_id({'id': data['user_id']})
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_skeptics = []

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True

        if len(sighting['location']) < 1:
            flash("Location Required.", 'sighting')
            is_valid = False

        if len(sighting['what_happened']) < 1:
            flash("Description of sighting required.", 'sighting')
            is_valid = False

        if len(sighting['date']) < 1:
            flash("Date field required.", 'sighting')
            is_valid = False


        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, what_happened, date, num_of_sasquatch, user_id) VALUES (%(location)s, %(what_happened)s, %(date)s,%(num_of_sasquatch)s, %(user_id)s );"
        results = connectToMySQL(Sighting.db).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings"
        results = connectToMySQL(Sighting.db).query_db(query)
        all_sightings = []

        for row in results:
            row['date'] = row['date'].strftime("%m/%d/%Y")
            all_sightings.append(cls(row))
            
        return all_sightings

    @classmethod
    def get_sighting_by_id(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s"
        results = connectToMySQL(Sighting.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, date = %(date)s, num_of_sasquatch = %(num_of_sasquatch)s WHERE id = %(id)s;"
        results = connectToMySQL(Sighting.db).query_db(query, data)

        return results

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(Sighting.db).query_db(query, data)

        return results

    @classmethod
    def get_all_with_skeptics(cls,data):
        query = "SELECT * FROM sightings LEFT JOIN skeptics ON sightings.id = skeptics.sighting_id LEFT JOIN users ON skeptics.user_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(Sighting.db).query_db(query, data)
        this_sighting = cls(results[0])
        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at':row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_sighting.user_skeptics.append(user.User(user_data))
        return this_sighting

    @classmethod
    def add_skeptic(cls,data):
        query = "INSERT INTO skeptics (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s)"
        results = connectToMySQL(Sighting.db).query_db(query, data)

        return results

    @classmethod
    def remove_skeptic(cls,data):
        query = "DELETE FROM skeptics WHERE user_id = %(user_id)s and sighting_id = %(sighting_id)s;"
        results = connectToMySQL(Sighting.db).query_db(query, data)

        return results

