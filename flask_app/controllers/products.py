from flask_app.models.product import Product
from flask_app.models.user import User
from flask_app.models.product_cat import Category
from pprint import pprint
from flask import render_template,redirect,request,session,flash
from flask_app import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/paulanamwanje/Documents/Projects/flask_app/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/createProduct")
def create_product():
    data = { 
        "id": session["user_id"]
    }
    user = User.get_one_user(data)
    pprint(user)
    categories = Category.get_all_categories()
    return render_template("addproduct.html", user = user, categories = categories)

@app.route("/productadd", methods=['GET','POST'])
def save_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/createProduct')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/createProduct')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/createProduct')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "qty": request.form["qty"],
            "price": request.form["price"],
            "user_id": session["user_id"],
            "image_path": "/static/images/"+ filename
        }

        product_id = Product.add_Product(data)
        pprint(product_id)
        category_dict = {
            "category_id": request.form["category_id"],
            "product_id" : product_id
        }
        cat_id = Category.add_product_to_category(category_dict)
        pprint(cat_id)
    return redirect('/dashboard')

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    if 'user_id' not in session:
        return redirect('/logout')
    product_data = {
        "product_id": product_id
    }
    
    user_data = {
        "id": session['user_id']
    }
    return render_template("editProduct.html", product=Product.get_one_product(product_data), user= User.get_one_user(user_data))

@app.route("/product/update/<int:product_id>", methods=["POST"])
def update_product_details(product_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect(f'/product/update/{product_id}')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/createProduct')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/createProduct')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "qty": request.form["qty"],
        "price": request.form["price"],
        "image_path": "/static/images/"+ filename,
        "product_id": product_id
        }
    Product.update_product(data)
    return redirect("/dashboard")

@app.route("/product_delete/<int:product_id>")
def del_product(product_id):
    if 'user_id' not in session:
        return redirect('/logout')
    Product.delete_product({"product_id":product_id})
    return redirect('/dashboard')

# @app.route("/search", methods=['GET', 'POST'])
# def search_product():
#     product = request.form["product"]
#     cursor.execute("SELECT name from ")
