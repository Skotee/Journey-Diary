from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__database__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(50), nullable=False)


class journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique = True)
    title = db.Column(db.String(50), nullable=False)

class day(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer,db.ForeignKey("journey.id"), nullable=False, unique = True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(10000), nullable=False)

class image(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer,db.ForeignKey("day.id"), nullable=False, unique = True)
    extension = db.Column(db.String(50), nullable=False, unique = True)
