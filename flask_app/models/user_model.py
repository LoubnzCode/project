from flask_app.config.mysqlconnection import connectToMySQL
from flask import session,flash
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email = data['email']
        self.birthdate = data['birthdate']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def userLogin(cls,data):
        grant_access = False
        if not User.validateLogin(data):
            grant_access = False
            return grant_access
        
        query = "SELECT password FROM users WHERE email = %(email)s;"
        Qdata ={'email' : data['email']}
        results = connectToMySQL('i_sport_db').query_db(query, Qdata)
        
        if not results:
            flash("Invalid Email/Password","flash_login")
            grant_access = False
            return grant_access
        else:
            dbpassword = results[0]['password']

        if not bcrypt.check_password_hash(dbpassword, data['password']) :       
            flash("Invalid Email/Password","flash_login")
            grant_access = False
            return grant_access
        else:    
            query = "SELECT * FROM users WHERE email = %(email)s and password = %(password)s;"
            Qdata ={'email' : data['email'],
                    'password' : dbpassword}
            results = connectToMySQL('i_sport_db').query_db(query, Qdata)
        if results :
            grant_access = True
            session['user_id'] = results[0]['id']
            session['first_name'] = results[0]['first_name']
            session['logedIn'] = True
        return grant_access

    @classmethod
    def emailexist(cls,email):
        email_exist = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email' : email}
        results = connectToMySQL('i_sport_db').query_db(query, data)
        if results : 
            email_exist = True
        return email_exist

    @classmethod
    def validateRegistration(cls,data):
        is_valid = True
        if len(data['first_name']) <3 :
            flash("- First name must be at least 3 characters","flash_registration")
            is_valid = False

        if len(data['last_name']) <3 :
            flash("- last name must be at least 3 characters","flash_registration")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("- Invalid email address!","flash_registration")
            is_valid = False
        else:
            if User.emailexist(data['email']):
                flash("- There is an account already associated with this email address!","flash_registration")
                is_valid = False

        if  len(data['birthdate']) == 0:
            flash("- Birthdate must not be blank!","flash_registration")
            is_valid = False
            return is_valid  

        if  len(data['password']) == 0:
            flash("- password must be at least 8 characters!","flash_registration")
            is_valid = False
            return is_valid  

        if  len(data['password']) <8:
            flash("- Password must be at least 8 characters!","flash_registration")
            is_valid = False

        if not data['password'] == data['confirm_password']:
            flash("- Password does not match!","flash_registration")
            is_valid = False
        return is_valid  

    @classmethod
    def validateLogin(cls,data):
        is_valid = True

        if not EMAIL_REGEX.match(data['email']): 
            flash("- Invalid email address!","flash_login")
            is_valid = False

        if  len(data['password']) == 0:
            flash("- password must be at least 8 characters!","flash_login")
            is_valid = False
        return is_valid

    @classmethod
    def registerUser(cls,data):
        reg_sucessfull = False
        if  User.validateRegistration(data):

            regData={
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'birthdate' : data['birthdate'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
            query = "INSERT INTO users (first_name, last_name, email,birthdate, password) VALUES \
                (%(first_name)s,%(last_name)s,%(email)s,%(birthdate)s,%(password)s)"
            results = connectToMySQL('i_sport_db').query_db(query, regData)
            reg_sucessfull = True
            session['user_id'] = results
            session['first_name'] = data['first_name']
            session['logedIn'] = True
        return reg_sucessfull




