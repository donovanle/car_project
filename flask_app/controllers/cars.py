from ssl import HAS_TLSv1_1
from flask_app import app
from flask import render_template,redirect,request,flash, session
from flask_app.models.car import Car
from flask_app.models.user import User

@app.route("/new")
def new_car():
    if "user_id" not in session:
        return render_template("index.html")
    return render_template('newcar.html')

@app.route("/newcar", methods=['POST'])
def car_created():
    if "user_id" not in session:
        return render_template("index.html")
    if not Car.validate_car(request.form):
        return redirect('/new')
    Car.create_car(request.form)
    return redirect('/dashboard')

@app.route('/view/<int:car_id>')
def show_car(car_id):
    if "user_id" not in session:
        return render_template("index.html")
    data = {"id" : car_id}
    return render_template('show.html',car=Car.car_by_id(data))

@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    if "user_id" not in session:
        return render_template("index.html")
    data = {"id" : car_id}
    return render_template('editcar.html',car=Car.car_by_id(data))

@app.route("/edit", methods=['POST'])
def edit_success():
    if "user_id" not in session:
        return render_template("index.html")
    if not Car.validate_car(request.form):
        return redirect('/new')
    Car.update_car(request.form)
    return redirect('/dashboard')

@app.route('/delete/<int:car_id>')
def car_deleted(car_id):
    if "user_id" not in session:
        return render_template("index.html")
    data = {"id" : car_id} 
    Car.delete_car(data)   
    return redirect('/dashboard')
