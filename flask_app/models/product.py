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
        self.admin_id = data['admin_id']
