from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

class Car:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['users_id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.first_name =  data['first_name']
        self.last_name = data['last_name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create_car(cls, data):
        car = {
            'user_id' : data['users_id'],
            'price' : data['price'],
            'model' : data['model'],
            'make' : data['make'],
            'year' : data['year'],
            'description' : data['description'],
        }
        query = "INSERT INTO cars (users_id,price, model, make, year, description,  created_at, updated_at) " \
            "VALUES (%(user_id)s,%(price)s,%(model)s,%(make)s,%(year)s,%(description)s, NOW(), NOW());"
        return connectToMySQL('exam_schema').query_db(query, car)
    
    @classmethod
    def all_cars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.users_id = users.id ORDER by cars.id DESC;"
        results = connectToMySQL('exam_schema').query_db(query)
        cars = []
        for item in results:
            cars.append(cls(item))
            print(item)
        print(cars)
        return cars
    @classmethod
    def car_by_id(cls, data):
        query = "SELECT *, users.first_name FROM cars LEFT JOIN users ON cars.users_id = users.id WHERE cars.id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        print(results)
        if results:
            return cls(results[0])
    
    @classmethod
    def update_car(cls, data):
        car = {
            'car_id' : data['car_id'],
            'price' : data['price'],
            'model' : data['model'],
            'make' : data['make'],
            'year' : data['year'],
            'description' : data['description']
        }
        query = "UPDATE cars SET price = %(price)s, model=%(model)s , make =%(make)s, year =%(year)s, description = %(description)s WHERE id = %(car_id)s;"
        return connectToMySQL('exam_schema').query_db(query, car)
    
    @classmethod
    def delete_car(cls,data):
        query= "DELETE FROM cars WHERE id = %(id)s"
        return connectToMySQL('exam_schema').query_db(query, data)

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['price']) < 1:
            flash("*Price Required","newcar")
            is_valid = False
        if int(data['price']) <= 0:
            flash("*Price Needs to Be Greater Than $0","newcar")
            is_valid = False
        if len(data['model']) < 1:
            flash("*Model Required","newcar")
            is_valid = False
        if len(data['make']) < 1:
            flash("*Make Required","newcar")
            is_valid = False
        if len(data['year']) < 1:
            flash("*Year Required","newcar")
            is_valid = False
        if int(data['year']) <= 0:
            flash("*Year Needs to Be over 0","newcar")
            is_valid = False
        if len(data['description']) < 1:
            flash("*Description Required","newcar")
            is_valid = False
        return is_valid
