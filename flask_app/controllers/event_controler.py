from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.event_model import Event

@app.route('/dashboard') 
def dashboard():
    if session['logedIn'] == True:
        all_today_events = Event.today_events()
        future_events = Event.future_events()
        return render_template("dashboard.html",all_today_events = all_today_events,future_events = future_events)
    else:
        return redirect("/") 

@app.route('/createEvent') 
def createEvent():
    if session['logedIn'] == True:       
        return render_template("createEvent.html")
    else:
        return redirect("/") 

@app.route('/createEvent', methods=["POST"]) 
def createEventPost():
    if not Event.validate(request.form):
        return redirect("/createEvent")
    else:
        Event.create(request.form)        
        return redirect("/dashboard")

@app.route('/deleteEvent/<id>')
def delete(id):
    if session['logedIn'] == True:
        Event.delete(id)
        return redirect("/dashboard")
    else:
        return redirect('/') 

@app.route('/viewEvent/<id>')
def viewEvent(id):
    if session['logedIn'] == True:
        eventData = Event.getEvent(id)
        return render_template("viewEvent.html",eventData = eventData)
    else:
        return render_template('/') 

@app.route('/editEvent/<id>')
def editEvent(id):
    if session['logedIn'] == True:
        eventData = Event.getEvent(id)
        return render_template("editEvent.html",eventData = eventData)
    else:
        return render_template('/') 

@app.route('/editEvent/<id>', methods = ["POST"])
def editEventPost(id):
    if session['logedIn'] == True:
        if not Event.validate(request.form):
            return redirect("/editEvent/<id>")
        else: 
            Event.update(id,request.form)
            return redirect('/dashboard')  
    else:
        return redirect('/')  


@app.route('/searchEvent') 
def searchEvent():
    if session['logedIn'] == True:
        return render_template("searchEvent.html")
    else:
        return redirect("/")  