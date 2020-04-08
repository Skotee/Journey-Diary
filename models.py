from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import USERNAME,PASSWORD,ADDRESS,DATABASE

app = Flask("__database__")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+"/"+DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    journey = db.relationship(
        "journey", back_populates="user", cascade="all, delete-orphan")


class journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=True)
    title = db.Column(db.String(50), nullable=False, unique = True)
    user = db.relationship("user", back_populates="journey")
    day = db.relationship("day", back_populates="journey",
                          cascade="all, delete-orphan")


class day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer, db.ForeignKey(
        "journey.id", ondelete="CASCADE"), nullable=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    journey = db.relationship("journey", back_populates="day")
    image = db.relationship("image", back_populates="day",
                            cascade="all, delete-orphan")


class image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey(
        "day.id", ondelete="CASCADE"), nullable=True)
    extension = db.Column(db.String(50), nullable=False)
    day = db.relationship("day", back_populates="image")
