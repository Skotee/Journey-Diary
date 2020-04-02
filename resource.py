from flask import request, Response, redirect
from flask_restful import Resource
from models import user, journey, day, image, db, app, api
from sqlalchemy import exc
from utils import ModelBuilder
from datetime import datetime
import json

MASON = "application/vnd.mason+json"

'''
Users
'''

class UserCollection(Resource):

    def get(self):
        body = ModelBuilder(items=[])
        for us in user.query.all():
            item = ModelBuilder(username=us.username)
            item.add_control("self", api.url_for(UserItem, user=us.id))
            body["items"].append(item)
        
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")


    def post(self):
        if not request.json:
            return "", 415
        try:
            us = user(username=request.json["username"],
                        password=request.json["password"],
                        email=request.json["email"])
            db.session.add(us)
            db.session.commit()
        except KeyError:
            return "", 400
        except exc.IntegrityError:
            return "", 409
        return "", 201

class UserItem(Resource):

    def get(self, user):
        pass

    def put(self, user):
        pass

    def delete(self, user):
        pass

'''
Journeys
'''

class JourneysByUser(Resource):

    def get(self,user):
        body = ModelBuilder(items=[])
        for jo in journey.query.filter_by(user_id=user).all():
            item = ModelBuilder(title=jo.title)
            item.add_control("self", api.url_for(JourneyItem, user=user, journey=jo.id))
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self,user):
        if not request.json :
            return "", 415
        try:
            jo = journey(title=request.json["title"],
                        user_id = user)
            db.session.add(jo)
            db.session.commit()
        except KeyError:
            return "", 400
        except exc.IntegrityError:
            return "", 409
        return "", 201

class JourneyItem(Resource):

    def get(self, user, journey):
        pass

    def put(self, user, journey):
        pass

    def delete(self, user, journey):
        pass


'''
Days
'''

class DaysByJourney(Resource):

    def get(self, user, journey):
        body = ModelBuilder(items=[])
        for da in day.query.filter_by(journey_id=journey).all():
            item = ModelBuilder(date=da.date.strftime("%d-%m-%Y"))
            item.add_control("self", api.url_for(DayItem, user=user, journey=journey, day=da.id))
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self, user, journey):
        if not request.json :
            return "", 415
        try:
            da = day(date=request.json["date"],
                        description = request.json["description"],
                        journey_id = journey)
            db.session.add(da)
            db.session.commit()
        except KeyError:
            return "", 400
        except exc.IntegrityError:
            return "", 409
        return "", 201

class DayItem(Resource):

    def get(self, user, journey, day):
        pass

    def put(self, user, journey, day):
        pass

    def delete(self, user, journey, day):
        pass



'''
Images
'''

class ImagesByDay(Resource):

    def get(self, user, journey, day):
        body = ModelBuilder(items=[])
        for im in image.query.filter_by(day_id=day).all():
            item = ModelBuilder()
            stim = str(im.id) + "." + im.extension
            item.add_control("self", api.url_for(ImageItem, user=user, journey=journey, day=day, image=stim))
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self, user, journey, day):
        if not request.json :
            return "", 415
        try:
            im = image(extension = request.json["extension"], day_id = day)
            db.session.add(im)
            db.session.commit()
        except KeyError:
            return "", 400
        except exc.IntegrityError:
            return "", 409
        return "", 201

class ImageItem(Resource):

    def get(self, user, journey, day, image):
        pass

    def put(self, user, journey, day, image):
        pass

    def delete(self, user, journey, day, image):
        pass
