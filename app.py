from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from models import user, journey, day, image, db, app
from resource import UserCollection, UserItem

api = Api(app)

api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<user>/")