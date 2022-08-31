from itertools import product
from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.product import Product
from flask_app.models.user import User
from pprint import pprint

@app.route("/createProduct")
def create_product():
    data = { 
        "id": session["user_id"]
    }
    return render_template("addproduct.html", user = User.get_one_user(data))

@app.route("/productadd", methods=['POST'])
def save_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/createProduct')
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "qty": request.form["qty"],
        "price": request.form["price"],
        "user_id": session["user_id"]
    }

    product_id = Product.add_Product(data)
    pprint(product_id)
    return redirect('/dashboard')
