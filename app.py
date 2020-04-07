from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import user, journey, day, image, db, app, api
from resource import UserCollection, UserItem, JourneysByUser, JourneyItem, DaysByJourney, DayItem, ImagesByDay, ImageItem


api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<userid>/")

api.add_resource(JourneysByUser, "/api/users/<userid>/journeys/")
api.add_resource(JourneyItem, "/api/users/<userid>/journeys/<journeyid>/")

api.add_resource(DaysByJourney, "/api/users/<userid>/journeys/<journeyid>/days/")
api.add_resource(DayItem, "/api/users/<userid>/journeys/<journeyid>/days/<dayid>/")

api.add_resource(ImagesByDay, "/api/users/<userid>/journeys/<journeyid>/days/<dayid>/images/")
api.add_resource(ImageItem, "/api/users/<userid>/journeys/<journeyid>/days/<dayid>/images/<imageid>")
