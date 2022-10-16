from itertools import product
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


db = 'eCommerce'

class Product:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.qty = data['qty']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.image_path = data['image_path']

    @classmethod
    def add_Product(cls, data):
        query = "INSERT INTO products (name, description, qty, price, user_id, image_path) VALUES (%(name)s, %(description)s, %(qty)s, %(price)s, %(user_id)s, %(image_path)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @classmethod
    def get_one_product(cls,data):
        query = "SELECT * FROM products WHERE products.id =%(product_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_all_products(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL(db).query_db(query)
        pprint(results)
        products = []
        for product in results:
            products.append(cls(product))
        return products

    @classmethod
    def update_product(cls, data):
        query = "UPDATE products SET name=%(name)s, description=%(description)s, qty=%(qty)s, price=%(price)s, image_path=%(image_path)s WHERE id =%(product_id)s;"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def delete_product(cls,data):
        query = "DELETE FROM products WHERE id = %(product_id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_product(product):
        is_valid = True
        if (product['name']) == "":
            flash("name,  must be at least 3 characters.","productadd")
            is_valid = False
        if (product['description']) == "":
            flash("description,  must be at least 3 characters.","productadd")
            is_valid = False
        if (product['qty']) == "":
            flash("Input qty of the product.","productadd")
            is_valid = False
        if (product['price'])  == "":
            flash("Input Price of Product","addressadd")
            is_valid = False
        return is_valid

