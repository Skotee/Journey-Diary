from flask import request
from flask_restful import Resource
from models import user, journey, day, image, db, app
from sqlalchemy import exc

'''
Users
'''

class UserCollection(Resource):

    def get(self):
        return []

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
        pass

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
        pass

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
        pass

    def post(self, user, journey, day):
        if not request.json :
            return "", 415
        try:
            im = image(extension = request.json["extension"],
                        day_id = day)
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
