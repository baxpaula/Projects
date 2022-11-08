from flask_app.models.product import Product
from flask_app.models.user import User
from flask_app.models.product_cat import Category
from pprint import pprint
from flask import render_template,redirect,request,session,flash
from flask_app import app
import os


@app.route("/addNew_category_page")
def product_categoryAdd():
    return render_template('category.html')


@app.route("/category/add", methods=['POST'])
def save_category():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Category.validate_category(request.form):
        return redirect('/addNew_category_page')
    data = {
        "category_name": request.form["category_name"],
        "category_type": request.form["category_type"],
    }
    category_id = Category.add_new_category(data)
    pprint(category_id)
    return redirect("/dashboard")

