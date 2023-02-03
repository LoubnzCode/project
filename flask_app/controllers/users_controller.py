from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.event_model import Event

@app.route('/')
def loadLogin():
    return render_template("login.html")

@app.route('/register', methods=["POST"])
def register():
    if not User.registerUser(request.form):
        return redirect('/')
    else:              
        if session['logedIn'] == True:
            return redirect("/dashboard") 
        else:
            return redirect('/')  

@app.route('/login', methods=["POST"])
def login():
    if User.userLogin(request.form):        
        return redirect("/dashboard") 
    else:
        return redirect("/") 

@app.route('/userAccount') 
def userAccount():
    if session['logedIn'] == True:
        return render_template("userAccount.html")
    else:
        return redirect("/") 

@app.route('/logout') 
def logout():
    session['logedIn'] = False
    return redirect("/") 

    