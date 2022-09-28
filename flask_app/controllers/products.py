from flask_app.models.product import Product
from flask_app.models.user import User
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
    return render_template("addproduct.html", user = User.get_one_user(data))

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
    return redirect('/dashboard')
