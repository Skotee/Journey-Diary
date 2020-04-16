import json
import os
import pytest
import tempfile
import time
import datetime as dt
from json import dumps
from jsonschema import validate
from dateutil import parser
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from app import app, db
from models import user, journey, day, image

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    db.create_all()
    _populate_db()

    yield app.test_client()

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


def _populate_db():
    us = user(
            id=5,
            username="testuser5",
            password="testpassword", 
            email="testemail5"
        )

    db.session.add(us)

    jo = journey(
            id=5,
            title="testtitle5",
            user = us
        )
        
    db.session.add(jo)



    da = day(
        id=5,
        description = "description5",
        date = dt.datetime(2012, 3, 3, 10, 10, 10),
        journey_id = 5, 
        journey = jo

        )

    im = image(
        id = 5, 
        extension = "jpg", 
        day_id = 5, 
        day = da
        )



    db.session.add(da)

    for i in range(1, 4):
        u = user(
            id=i,
            username="testuser"+str(i),
            password="testpassword", 
            email="testemail"+str(i)
        )

        db.session.add(u)

    for i in range(1, 4):
        j = journey(
            id=i,
            title="testtitle"+str(i),
            user = us
        )

        db.session.add(j)

    for i in range(1, 4):
        d = day(
            id=i,
            description = "description"+str(i),
            journey_id = 5, 
            date = dt.datetime(2012, 3, 3, 10, 10, 10)
        )

        db.session.add(d)

    for i in range(1, 4):
        i = image(
            id=i,
            extension="jpg",
            day_id = 5
        )

        db.session.add(i)


    db.session.commit()

    
def _get_user_json(number=1):
    """
    Creates a valid sensor JSON object to be used for PUT and POST tests.
    """
    
    return {"id": 1, "username": "extrauser", "password":"extrapassword", "email":"extraemail" }

def _get_unvalid_user_json(number=1):
    """
    Creates a valid sensor JSON object to be used for PUT and POST tests.
    """
    
    return {"id": 10, "username": "extrauser", "password":"extrapassword", "email":"extraemail" }

def _get_journey_json(number=1):
    """
    Creates a valid sensor JSON object to be used for PUT and POST tests.
    """
    
    return {"id": 1, "title": "extratitle"}

def _get_day_json(number=1):
    """
    Creates a valid sensor JSON object to be used for PUT and POST tests.
    """
    
    return {"id": 1, "description": "extradescription", "date":dt.datetime(2012, 3, 3, 10, 10, 10), "journey_id": 5}

def _get_image_json(number=1):
    """
    Creates a valid sensor JSON object to be used for PUT and POST tests.
    """
    
    return {"id": 1, "extension": "jpg", "day_id": 5}   
    
    
    
def _check_namespace(client, response):
    """
    Checks that the "self" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """
    
    ns_href = response["@namespaces"]["journeydiary"]["id"]
    resp = client.get(ns_href)
    assert resp.status_code == 200
    
def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200
    
def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """
    
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204
    
def _check_control_put_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_user_json()
    body["id"] = obj["id"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204
    
def _check_control_post_method_user(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_user_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201


def _check_control_post_method_journey(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_journey_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

class TestUserCollection(object):
    """
    This class implements tests for each HTTP method in user collection
    resource. 
    """
    
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_control_post_method_user("add", client, body)
        assert len(body["items"]) == 4
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            assert "username" in item


    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        
        valid = _get_user_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        assert resp.status_code == 201
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["username"] == "extrauser"
        assert body["email"] == "extraemail"

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove username field for 400
        valid.pop("username")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

  
        
        
class TestUserItem(object):
    
    RESOURCE_URL = "/api/users/1/"
    INVALID_URL = "/api/users/X/"
    MODIFIED_URL = "/api/users/1/"
    
    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["username"] == "testuser1"
        assert body["email"] == "testemail1"
        _check_control_delete_method("delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible errors codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the user can be found from a its new URI. 
        """
        
        valid = _get_user_json()
        
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another id
        valid["username"] = "extrauser"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
 
             
        # test with valid (only change id)
        valid["username"] = "testuser2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
           
        # remove field for 400
        valid.pop("username")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_user_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
      
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestJourneybyUser(object):
    """
    This class implements tests for each HTTP method in user collection
    resource. 
    """
    
    RESOURCE_URL = "/api/users/5/journeys/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_control_post_method_journey("add", client, body)
        assert len(body["items"]) == 4
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            assert "title" in item


    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        
        valid = _get_journey_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        assert resp.status_code == 201
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["title"] == "extratitle"

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # remove username field for 400
        valid.pop("title")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

       
        
        
class TestJourneyItem(object):
    
    RESOURCE_URL = "/api/users/5/journeys/2/"
    INVALID_URL = "/api/users/X/journeys/X/"
    MODIFIED_URL = "/api/users/5/journeys/1/"
    
    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["title"] == "testtitle2"
        _check_control_delete_method("delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible errors codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the user can be found from a its new URI. 
        """
        
        valid = _get_journey_json()
        
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another id
        valid["title"] = "extratitle"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
 
           
        # remove field for 400
        valid.pop("title")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_journey_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
      
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestDayByJourney(object):
    """
    This class implements tests for each HTTP method in user collection
    resource. 
    """
    
    RESOURCE_URL = "/api/users/5/journeys/5/days/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            assert "date" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        
        valid = _get_day_json()
        day = valid["date"]
        d = day.isoformat()
        valid["date"] = d
        

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        assert resp.status_code == 201
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["description"] == "extradescription"

        # test with wrong content type

        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # remove username field for 400
        valid.pop("description")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        
class TestDayItem(object):
    
    RESOURCE_URL = "/api/users/5/journeys/5/days/1/"
    INVALID_URL = "/api/users/X/journeys/X/days/X/"
    MODIFIED_URL = "/api/users/5/journeys/5/days/2/"
    
    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["description"] == "description1"
        _check_control_delete_method("delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible errors codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the user can be found from a its new URI. 
        """
        
        valid = _get_day_json()
        day = valid["date"]
        d = day.isoformat()
        valid["date"] = d

        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another id
        valid["description"] = "extradescription"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
            
        # remove field for 400
        valid.pop("description")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_day_json()
        day = valid["date"]
        d = day.isoformat()
        valid["date"] = d
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
      
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestImagesByDay(object):
    """
    This class implements tests for each HTTP method in user collection
    resource. 
    """
    
    RESOURCE_URL = "/api/users/5/journeys/5/days/5/images/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        
        valid = _get_image_json()
       
        

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        assert resp.status_code == 201
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)

        # test with wrong content type

        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # remove username field for 400
        valid.pop("extension")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        
class TestImageItem(object):

    
    RESOURCE_URL = "/api/users/5/journeys/5/days/5/images/1"
    INVALID_URL = "/api/users/X/journeys/X/days/X/images/X"
    MODIFIED_URL = "/api/users/5/journeys/5/days/5/images/2"
    
    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible errors codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the user can be found from a its new URI. 
        """
        
        valid = _get_image_json()
      
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another id
        valid["extension"] = "jpg"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
            
        # remove field for 400
        valid.pop("extension")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_image_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
      
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        





