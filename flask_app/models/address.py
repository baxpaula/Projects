from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from pprint import pprint

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
        self.users = None

    @classmethod
    def add_address(cls,data):
        query = "INSERT INTO addresses (street, city, state, zip, user_id) VALUES (%(street)s, %(city)s, %(state)s, %(zip)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results


    @classmethod
    def get_user_address(cls,data):
        query = "SELECT * FROM users JOIN addresses on addresses.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        pprint(results)
        if results:
            userAddress = cls(results[0])
            for row_from_db in results:
                print(row_from_db)
                user_data = {
                    'id' : row_from_db['id'],
                    'first_name' : row_from_db['first_name'],
                    'last_name' : row_from_db['last_name'],
                    'email' : row_from_db['email'],
                    'password' : row_from_db['password'],
                    'id': row_from_db['addresses.id'],
                    "street": row_from_db['street'],
                    "city": row_from_db['city'],
                    "state": row_from_db['state'],
                    "zip": row_from_db['zip'],
                    'created_at' : row_from_db['addresses.created_at'],
                    "updated_at" : row_from_db["addresses.updated_at"]
                }
                
                userAddress.users = (user.User(user_data))
                pprint(userAddress)
            return userAddress
        return False

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
