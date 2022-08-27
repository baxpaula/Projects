from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register',methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    
    session['user_id'] = User.save(data)
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one_user(user_data)
    return render_template('dashboard.html', user = user)

@app.route('/update/<int:user_id>',methods=['POST'])
def update(user_id):
    data ={ 
        "id": user_id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "dob": request.form['dob'],
        "ustreet": request.form['ustreet'],
        "uapt": request.form['uapt'],
        "ucity": request.form['ucity'],
        "ustate": request.form['ustate'],
        "uzip": request.form['uzip']
    }
    
    User.update(data)
    user_session = session['user_id']
    return redirect ('/success/'+ str(user_session))

@app.route('/loginPage')
def loginUser():
    return render_template('loginpage.html')

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/success/<int:user_id>')
def edit(user_id):
    data = { 
        "id": user_id
    }

    return render_template("account_page.html", user = User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')