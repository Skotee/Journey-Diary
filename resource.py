from flask import request, Response, redirect
from flask_restful import Resource
from models import user, journey, day, image, db, app, api
from sqlalchemy import exc
from utils import ModelBuilder
import datetime as dt
from jsonschema import validate, ValidationError
import json
import utils

MASON = "application/vnd.mason+json"



class UserCollection(Resource):

    def get(self):
        body = ModelBuilder(items=[])
        for us in user.query.all():
            item = ModelBuilder(username=us.username)
            item.add_control("self", api.url_for(UserItem, userid=us.id))
            body["items"].append(item)
        body.add_controls_users_coll()
        
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")


    def post(self):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, utils.user_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        try:
            us = user(username=request.json["username"], password=request.json["password"], email=request.json["email"])
            db.session.add(us)
            db.session.commit()
        except KeyError:
            return utils.create_error_response(400, "Key Error", "Bad parameters")
        except exc.IntegrityError:
            return utils.create_error_response(409, "Already exists", "User with username " + str(request.json["username"]) + " or email " + str(request.json["email"]) + " already exists.")
        uri = api.url_for(UserItem, userid = us.id)
        resp = Response(status=201, headers={"Location": uri})
        return resp

class UserItem(Resource):

    def get(self, userid):
        us = user.query.filter_by(id = userid).first()
        if us is None: 
            return utils.create_error_response(404, "User not found", "User with the id "+ userid +" doesn't exist")
        body = ModelBuilder(username = us.username, email = us.email)
        body.add_controls_user_item(userid)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, userid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type","Requests must be JSON")
        us = user.query.filter_by(id = userid).first()
        if us is None: 
            return utils.create_error_response(404, "User not found", "User with the id "+ userid +" doesn't exist")
        try:
            validate(request.json, utils.user_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        us.username = request.json["username"]
        us.password = request.json["password"]
        us.email = request.json["email"]
        try:
            db.session.commit()
        except exc.IntegrityError:
            return utils.create_error_response(409, "Already exists", "User with username " + str(request.json["username"]) + " already exists.")
        uri = api.url_for(UserItem, userid = us.id)
        resp = Response(status=204, headers={"Location": uri})
        return resp

    def delete(self, userid):
        us = user.query.filter_by(id = userid).first()
        if us is None: 
            return utils.create_error_response(404, "User not found", "User with the id "+ userid +" doesn't exist")
        db.session.delete(us)
        try:
            db.session.commit()
        except exc.IntegrityError:
            return utils.create_error_response(409, "IntegrityError", "IntegrityError")
        body = ModelBuilder()
        return Response(json.dumps(body), 204, mimetype="application/vnd.mason+json")




class JourneysByUser(Resource):

    def get(self, userid):
        body = ModelBuilder(items=[])
        us = user.query.filter_by(id = userid).first()
        if us is None:
            return utils.create_error_response(404, "User not found", "User with the id "+ userid +" doesn't exist")
        for jo in journey.query.filter_by(user_id=userid).all():
            item = ModelBuilder(title=jo.title)
            item.add_control("self", api.url_for(JourneyItem, userid=userid, journeyid=jo.id))
            body["items"].append(item)
        body.add_controls_journeys_coll(userid)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self, userid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, utils.journey_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        jo = journey(title=request.json["title"], user_id = userid)

        us = user.query.filter_by(id = jo.user_id).first()
        if us is None:
            return utils.create_error_response(404, "User not found", "User with the id "+ userid +" doesn't exist")
        try:
            db.session.add(jo)
            db.session.commit()
        except KeyError:
            return utils.create_error_response(400, "Key Error", "Bad parameters")
        uri = api.url_for(JourneyItem, userid = userid, journeyid = jo.id)
        resp = Response(status=201, headers={"Location": uri})
        return resp

class JourneyItem(Resource):

    def get(self, userid, journeyid):
        jo = journey.query.join(user).filter(
                journey.id == journeyid,
                user.id == userid
            ).first()
        if jo is None: 
            return utils.create_error_response(404, "Journey not found", "Journey doesn't exist")
        body = ModelBuilder(title = jo.title)
        body.add_controls_journey_item(userid, journeyid)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, userid, journeyid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type","Requests must be JSON")
        jo = journey.query.join(user).filter(
                journey.id == journeyid,
                user.id == userid
            ).first()
        if jo is None: 
            return utils.create_error_response(404, "Journey not found", "Journey doesn't exist")
        try:
            validate(request.json, utils.journey_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        jo.title = request.json["title"]
        db.session.commit()
        uri = api.url_for(JourneyItem, userid = userid, journeyid = jo.id)
        resp = Response(status=204, headers={"Location": uri})
        return resp


    def delete(self, userid, journeyid):
        jo = journey.query.join(user).filter(
                journey.id == journeyid,
                user.id == userid
            ).first()
        if jo is None: 
            return utils.create_error_response(404, "Journey not found", "Journey doesn't exist")
        db.session.delete(jo)
        db.session.commit()
        body = ModelBuilder()
        return Response(json.dumps(body), 204, mimetype="application/vnd.mason+json")





class DaysByJourney(Resource):

    def get(self, userid, journeyid):
        jo = journey.query.join(user).filter(
                journey.id == journeyid,
                user.id == userid
            ).first()
        if jo is None: 
            return utils.create_error_response(404, "Journey not found", "Journey doesn't exist")
        body = ModelBuilder(items=[])
        for da in day.query.filter_by(journey_id=journeyid).all():
            item = ModelBuilder(date=da.date.strftime("%d-%m-%Y"))
            item.add_control("self", api.url_for(DayItem, userid=userid, journeyid=journeyid, dayid=da.id))
            body["items"].append(item)
        body.add_controls_days_coll(userid, journeyid)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self, userid, journeyid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, utils.day_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        jo = journey.query.join(user).filter(
                journey.id == journeyid,
                user.id == userid
            ).first()
        if jo is None: 
            return utils.create_error_response(404, "Journey not found", "Journey doesn't exist")
        try:
            da = day(date= dt.datetime.strptime(request.json["date"], "%Y-%m-%dT%H:%M:%S"), description = request.json["description"], journey_id = journeyid)
            db.session.add(da)
            db.session.commit()
        except KeyError:
            return utils.create_error_response(400, "Key Error", "Bad parameters")
        uri = api.url_for(DayItem, userid = userid, journeyid = journeyid, dayid = da.id)
        resp = Response(status=201, headers={"Location": uri})
        return resp

class DayItem(Resource):

    def get(self, userid, journeyid, dayid):
        da = day.query.join(journey).join(user).filter(
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if da is None:
            return utils.create_error_response(404, "Day not found", "Day doesn't exist")
        body = ModelBuilder(date = da.date.strftime("%d-%m-%Y"), description = da.description)
        body.add_controls_day_item(userid, journeyid, dayid)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, userid, journeyid, dayid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type","Requests must be JSON")
        da = day.query.join(journey).join(user).filter(
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if da is None:
            return utils.create_error_response(404, "Day not found", "Day doesn't exist")
        try:
            validate(request.json, utils.day_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        da.date = dt.datetime.strptime(request.json["date"], "%Y-%m-%dT%H:%M:%S")
        da.description = request.json["description"]
        db.session.commit()
        uri = api.url_for(DayItem, userid = userid, journeyid = journeyid, dayid = da.id)
        resp = Response(status=204, headers={"Location": uri})
        return resp

    def delete(self, userid, journeyid, dayid):
        da = day.query.join(journey).join(user).filter(
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if da is None:
            return utils.create_error_response(404, "Day not found", "Day doesn't exist")
        db.session.delete(da)
        db.session.commit()
        body = ModelBuilder()
        return Response(json.dumps(body), 204, mimetype="application/vnd.mason+json")





class ImagesByDay(Resource):

    def get(self, userid, journeyid, dayid):
        da = day.query.join(journey).join(user).filter(
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if da is None:
            return utils.create_error_response(404, "Day not found", "Day doesn't exist")
        body = ModelBuilder(items=[])
        for im in image.query.filter_by(day_id=dayid).all():
            item = ModelBuilder()
            stim = str(im.id) + "." + im.extension
            item.add_control("self", api.url_for(ImageItem, userid=userid, journeyid=journeyid, dayid=dayid, imageid=stim))
            body["items"].append(item)
        body.add_controls_images_coll(userid, journeyid, dayid)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self, userid, journeyid, dayid):
        da = day.query.join(journey).join(user).filter(
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if da is None:
            return utils.create_error_response(404, "Day not found", "Day doesn't exist")
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, utils.image_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        try:
            im = image(extension = request.json["extension"], day_id = dayid)
            db.session.add(im)
            db.session.commit()
        except KeyError:
            return utils.create_error_response(400, "Key Error", "Bad parameters")
        uri = api.url_for(ImageItem, userid = userid, journeyid = journeyid, dayid = dayid, imageid = im.id)
        resp = Response(status=201, headers={"Location": uri})
        return resp

class ImageItem(Resource):

    def get(self, userid, journeyid, dayid, imageid):
        im = image.query.join(day).join(journey).join(user).filter(
                image.id == imageid,
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if im is None:
            return utils.create_error_response(404, "Image not found", "Image doesn't exist")
        stim = str(im.id) + "." + im.extension
        body = ModelBuilder(image = stim)
        body.add_controls_image_item(userid, journeyid, dayid, imageid)
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")


    def put(self, userid, journeyid, dayid, imageid):
        if not request.json:
            return utils.create_error_response(415, "Unsupported media type","Requests must be JSON")
        im = image.query.join(day).join(journey).join(user).filter(
                image.id == imageid,
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if im is None:
            return utils.create_error_response(404, "Image not found", "Image doesn't exist")
        try:
            validate(request.json, utils.image_schema())
        except ValidationError as e:
            return utils.create_error_response(400, "Invalid JSON document", str(e))
        im.extension = request.json["extension"]
        db.session.commit()
        uri = api.url_for(ImageItem, userid = userid, journeyid = journeyid, dayid = dayid, imageid = im.id)
        resp = Response(status=204, headers={"Location": uri})
        return resp

    def delete(self, userid, journeyid, dayid, imageid):
        im = image.query.join(day).join(journey).join(user).filter(
                image.id == imageid,
                day.id == dayid,
                journey.id == journeyid,
                user.id == userid
            ).first()
        if im is None:
            return utils.create_error_response(404, "Image not found", "Image doesn't exist")
        db.session.delete(im)
        db.session.commit()
        body = ModelBuilder()
        return Response(json.dumps(body), 204, mimetype="application/vnd.mason+json")
