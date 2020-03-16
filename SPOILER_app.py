
from flask import Flask
from flask import request
from flask_restful import Api
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc



app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class ProductCollection(Resource):

    def get(self):
        return db.session.query(Product).first()
 

    def post(self):

            
        try:

            if not request.json:
                return "", 415
            #if not ((type(request.json["handle"]) is str) and ((type(request.json["weight"]) is str) or (type(request.json["weight"]) is float)) and (type(request.json["price"]) is float)):
            if not ((type(request.json["handle"]) is str) and (type(request.json["weight"]) is float) and (type(request.json["price"]) is float)):
                return "", 400
            product = Product(
                handle=request.json["handle"],
                weight=request.json["weight"],
                price=request.json["price"])
            db.session.add(product)
            db.session.commit()
        except KeyError:
            return "", 400
        except exc.IntegrityError:
            return "", 409
        
        return "", 201


class ProductItem(Resource):

    def get(self, product):
        pass

    def put(self, product):
        pass

    def delete(self, product):
        pass

class Product(db.Model):
    handle = db.Column(db.String(50), primary_key=True)
    weight = db.Column(db.Float(), nullable = False)
    price = db.Column(db.Float(), nullable=False)

api.add_resource(ProductCollection, "/api/products/")
api.add_resource(ProductItem, "/api/products/<product>/")

