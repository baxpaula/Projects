from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = 'eCommerce'

class Address:
    def __init__(self, data):
        self.id = data['id']
        self.street = data['street']
        self.city= data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def add_address(cls,data):
        query = "INSERT INTO addresses (street, city, state, zip, user_id) VALUES (%(street)s, %(city)s, %(state)s, %(zip)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results




    @staticmethod
    def validate_address(address):
        is_valid = True
        if (address['street']) == "":
            flash("Input make,  must be at least 3 characters.","addressadd")
            is_valid = False
        if (address['city']) == "":
            flash("Input make,  must be at least 3 characters.","addressadd")
            is_valid = False
        if (address['state']) == "":
            flash("Input make,  must be at least 3 characters.","addressadd")
            is_valid = False
        if len(address['zip']) < 5:
            flash("Please input proper zip code","addressadd")
            is_valid = False
        return is_valid
