from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import product


db = 'eCommerce'

class Category:
    def __init__( self , data ):
        self.id = data['id']
        self.category_name = data['category_name']
        self.category_type = data['category_type']
    
    
    @classmethod
    def add_new_category(cls,data):
        query = "INSERT INTO categories (category_name,category_type) VALUES (%(category_name)s, %(category_type)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @classmethod
    def get_all_categories(cls):
        query = "SELECT * FROM categories;"
        results = connectToMySQL(db).query_db(query)
        categories = []
        for cat in results:
            categories.append(cls(cat))
        return categories

    @classmethod
    def add_product_to_category(cls,data):
        query = "INSERT INTO categorizations (category_id, product_id) VALUES (%(category_id)s, %(product_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_category(category):
        is_valid = True
        if (category['category_name']) == "":
            flash("category_name,  must be at least 3 characters.","categoryadd")
            is_valid = False
        if (category['category_type']) == "":
            flash("category type,  must be at least 3 characters.","categoryadd")
            is_valid = False
        return is_valid