from flask_restful import Resource
from models import user, journey, day, image, db, app

class UserCollection(Resource):

    def get(self):
        return []

    def post(self):
        if not request.json:
            abort(415)
            
        try:
            us = user(username=request.json["handle"],
                        password=request.json["weight"],
                        email=request.json["price"])
            db.session.add(us)
            db.session.commit()
        except KeyError:
            abort(400)
        except IntegrityError:
            abort(409)
        
        return "", 201


class UserItem(Resource):

    def get(self, product):
        pass

    def put(self, product):
        pass

    def delete(self, product):
        pass
