from flask_app.config.mysqlconnection import connectToMySQL
from flask import session,flash
from flask_app import app

class Event:
    def __init__( self , data ):
        self.id = data['id'] 
        self.user_id = data['user_id']
        self.event_name = data['event_name']
        self.location_name  = data['location_name']
        self.event_date  = data['event_date']        
        self.time = data['time']
        self.infomation = data['infomation']
        self.capacity = data['capacity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def validate(cls,data):
        is_valid = True
        if len(data['event_name']) <3 :
            flash("-Event name must be at least 3 characters","flash_CreateNewEvent")
            is_valid = False

        if len(data['location_name']) <3 :
            flash("-Location name must be at least 3 characters","flash_CreateNewEvent")
            is_valid = False

        if  len(data['event_date']) == 0:
            flash("-Event date must not be blank!","flash_CreateNewEvent")
            is_valid = False
            return is_valid 

        if  len(data['time']) == 0:
            flash("-Starting time must not be blank!","flash_CreateNewEvent")
            is_valid = False
            return is_valid  

        if  len(data['infomation']) <1:
            flash("-Event details must not be blank!","flash_CreateNewEvent")
            is_valid = False
            return is_valid  

        if  int(data['capacity']) == 0:
            flash("-Capacity must not be 0 or blank!","flash_CreateNewEvent")
            is_valid = False
        return is_valid

    @classmethod
    def create(cls,data):                 
        qdata = {'event_name':data['event_name'],
                'user_id':session['user_id'],
                'location_name':data['location_name'],
                'event_date':data['event_date'],
                'time':data['time'],
                'infomation':data['infomation'],
                'capacity':data['capacity']} 
        query = "INSERT INTO events (event_name,user_id, location_name, time,event_date,infomation, capacity) VALUES \
                (%(event_name)s,%(user_id)s,%(location_name)s,%(time)s,%(event_date)s,%(infomation)s,%(capacity)s)"
        results = connectToMySQL('i_sport_db').query_db(query, qdata)
        return results

    @classmethod
    def update(cls,id,data):                 
        qdata = {'id':id,
                'event_name':data['event_name'],
                'location_name':data['location_name'],
                'event_date':data['event_date'],
                'time':data['time'],
                'infomation':data['infomation'],
                'capacity':data['capacity']} 
        query = "UPDATE events SET  event_name = %(event_name)s,\
                                    location_name = %(location_name)s,\
                                    event_date = %(event_date)s,\
                                    time = %(time)s,\
                                    infomation = %(infomation)s,\
                                    capacity = %(capacity)s\
                                WHERE id = %(id)s"
        results = connectToMySQL('i_sport_db').query_db(query, qdata)
        return results

    @classmethod
    def getEvent(cls,id): 
        data = {'id' : id}        
        query = "SELECT * FROM events WHERE id = %(id)s"
        results = connectToMySQL('i_sport_db').query_db(query, data)
        return results

    @classmethod
    def delete(cls,id): 
        data = {'id' : id}        
        query = "DELETE FROM events WHERE id = %(id)s"
        results = connectToMySQL('i_sport_db').query_db(query, data)
        return results

    @classmethod
    def today_events(cls):  
        qdata = {'user_id':session['user_id']} 
        query = "SELECT * FROM events WHERE user_id = %(user_id)s AND event_date = curdate()"
        results = connectToMySQL('i_sport_db').query_db(query, qdata)
        return results

    @classmethod
    def future_events(cls):  
        qdata = {'user_id':session['user_id']} 
        query = "SELECT * FROM events WHERE user_id = %(user_id)s AND event_date > curdate()"
        results = connectToMySQL('i_sport_db').query_db(query, qdata)
        return results

