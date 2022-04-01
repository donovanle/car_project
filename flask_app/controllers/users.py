from flask_app import app
from flask import render_template,redirect,request,flash, session
from flask_app.models.user import User
from flask_app.models.car import Car

from flask_app.controllers.cars import *


#homepage
@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html")
    else:
        return redirect('/dashboard')

#register form
@app.route("/register", methods=["POST"])
def saveuser():
    if not User.validate_register_user(request.form):
        return redirect('/')
    if not User.email_is_valid(request.form):
        return redirect('/')
    user_id = User.createuser(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')


#login form
@app.route('/login', methods=["POST"])
def login():
    if User.validate_login(request.form):
        data = {"email": request.form['email']}
        user = User.user_email(data)
        session['user_id'] = user.id
        return redirect('/dashboard')
    else:
        return redirect('/')

# dashboard page displays hello name of user
@app.route("/dashboard")
def loggedin():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session['user_id']}
    return render_template("dashboard.html", user = User.user_id(data),car_list= Car.all_cars(), user_id=session['user_id'])

# clear session/logout of current user
@app.route('/logout') 
def index_two():
    session.clear()
    return redirect('/')