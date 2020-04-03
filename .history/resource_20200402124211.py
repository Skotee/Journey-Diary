from flask import request
from flask_restful import Resource
from models import user, journey, day, image, db, app
from sqlalchemy import exc

'''
Users
'''

class UserCollection(Resource):

    def get(self):
        db_user = User.query.first()
        if db_user is None:
            return create_error_response(404, "Not found", 
                "No sensor was found with the name {}".format(product)
            )
        body = InventoryBuilder()
        body.add_namespace("prohub", LINK_RELATIONS_URL)
        body.add_control("profile", USER_PROFILE)
        body.add_control_add_user()
        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def post(self):
        if not request.json:
            return "", 415
        try:
            validate(request.json, self.get_schema())
        except ValidationError as e:
            return self.create_error_response(400, "Invalid JSON document", str(e))

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
        db_user = User.query.first()
        if db_user is None:
            return create_error_response(404, "Not found", 
                "No sensor was found with the name {}".format(product)
            )

        body = InventoryBuilder(
            handle = request.json["handle"],
            weight = request.json["weight"],
            price = request.json["price"]
            )

        body.add_namespace("prohub", LINK_RELATIONS_URL)
        body.add_control("profile", USER_PROFILE)
        body.add_control("item", UserCollection)
        body.add_control_edit_user(self,handle)
        body.add_control_delete_user(self,handle)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, user):
        if not request.json:
            return self.create_error_response(415, "Unsupported media type",
                "Requests must be JSON"
            )
        if User.query.filter_by(handle=handle).first() is None: 
        	return self.create_error_response(415, "User not found",
                "User doesn't exists"
            )

        try:
            validate(request.json, self.get_schema())
        except ValidationError as e:
            return self.create_error_response(400, "Invalid JSON document", str(e))

        try:
            User.query.filter_by(handle=handle).first().update({"weight":request.json["weight"]})
            User.query.filter_by(handle=handle).first().update({"price":request.json["price"]})
            db.session.commit()
        except IntegrityError:
            return self.create_error_response(409, "Already exists", 
                "User with handle " + request.json["handle"] + " already exists.".format(request.json["handle"])
            )
        
        return Response(status=201, headers={
            "Location": api.url_for(UserItem, user=user.handle)
        })

    def delete(self, user):
        pass

'''
Journeys
'''

class JourneyCollection(Resource):

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

class DayCollection(Resource):

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

class ImageCollection(Resource):

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
