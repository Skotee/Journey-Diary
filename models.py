from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask("__database__")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Journey111@127.0.0.1/sys"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(50), nullable=False)
    journey = db.relationship("journey", back_populates="user")


class journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    user = db.relationship("user", back_populates="journey")
    day = db.relationship("day", back_populates="journey")


class day(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer,db.ForeignKey("journey.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    journey = db.relationship("journey", back_populates="day")
    image = db.relationship("image", back_populates="day")


class image(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer,db.ForeignKey("day.id",ondelete="CASCADE"), nullable=False)
    extension = db.Column(db.String(50), nullable=False)
    day = db.relationship("day", back_populates="image")
