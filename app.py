from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from models import user, journey, day, image, db, app
from resource import UserCollection, UserItem, JourneyCollection, JourneyItem, DayCollection, DayItem, ImageCollection, ImageItem

api = Api(app)

api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<user>/")

api.add_resource(JourneysByUser, "/api/users/<user>/journeys/")
api.add_resource(JourneyItem, "/api/users/<user>/journeys/<journey>/")

api.add_resource(DaysByJourney, "/api/users/<user>/journeys/<journey>/days/")
api.add_resource(DayItem, "/api/users/<user>/journeys/<journey>/days/<day>/")

api.add_resource(ImagesByDay, "/api/users/<user>/journeys/<journey>/days/<day>/images/")
api.add_resource(ImageItem, "/api/users/<user>/journeys/<journey>/days/<day>/images/<image>")
