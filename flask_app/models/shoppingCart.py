from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import product
from flask_app.models import product_cat

db = 'eCommerce'

class ShoppingCart:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_to_shopping_cart(cls,data):
        query = "INSERT INTO shoppingCart (user_id) VALUES (%(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @classmethod
    def add_product_to_cart(cls,data):
        query = "INSERT INTO products_has_shoppingCart (product_id, shoppingCart_id) VALUES (%(product_id)s, %(shoppingCart_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results