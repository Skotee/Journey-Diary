import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

import app
from app import user, journey, day, image

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db
    
    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

    """
Function for creating a user
    """
def _get_user(): 
    return user(
        id = 4444,
        username ="Maella",
        password = "mmmm" ,
        email ="maella.gheraia@gmail.com"
    )
    """
Function for creating a journey
    """
 
def _get_journey(): 
    return journey(
        id = 5555,
        user_id = 4444,
        title ="Journey test"
    )
    """
Function for creating a day
    """
def _get_day(): 
    return day(
        id = 6666,
        journey_id = 5555,
        date = datetime.now() ,
        description ="Nice trip"
    )
    """
Function for creating an image
    """
def _get_image(): 
    return image(
        id = 7777,
        day_id = 6666,
        extension = "jpg" 
    )
    """
Function for adding a user in the database
    """
def test_create_user(db_handle): 
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    assert user.query.count() == 1
    assert user.query.first() == u
 
    """
Function for deleting a user from the database
 
    """
def test_delete_user(db_handle):
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.delete(u)
    assert user.query.count() == 0
 
    """
Function for adding a journey in the database
 
 
    """
def test_create_journey(db_handle):  
    j = _get_journey()
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    assert journey.query.count() == 1
    assert journey.query.first() == j
 
    """
Function for deleting a journey from the database
 
    """
def test_delete_journey(db_handle): 
    j = _get_journey()
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.delete(j)
    assert journey.query.count() == 0
    """
Function for adding a day in the database
 
    """
def test_create_day(db_handle):
    j = _get_journey()
    u = _get_user()
    d = _get_day()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.add(d)
    db_handle.session.commit()
    assert day.query.count() == 1
    assert day.query.first() == d
 
    """
Function for deleting a day in the database
 
    """
def test_delete_day(db_handle):
    j = _get_journey()
    u = _get_user()
    d = _get_day()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.add(d)
    db_handle.session.commit()
    db_handle.session.delete(d)
    assert day.query.count() == 0
    """
Function for adding an image in the database
 
    """
def test_create_image(db_handle):
    j = _get_journey()
    u = _get_user()
    d = _get_day()
    i = _get_image()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.add(d)
    db_handle.session.commit()
    db_handle.session.add(i)
    db_handle.session.commit()
    assert image.query.count() == 1
    assert image.query.first() == i
 
    """
Function for deleting an image in the database
 
    """
def test_delete_image(db_handle):
    j = _get_journey()
    u = _get_user()
    d = _get_day()
    i = _get_image()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.add(d)
    db_handle.session.commit()
    db_handle.session.add(i)
    db_handle.session.commit()
    db_handle.session.delete(i)
    assert image.query.count() == 0
    """
Function for updating the email of a user
 
    """
def test_update_user(db_handle): 
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    user.query.filter_by(id=4444).update(dict(email='my_new_email@example.com'))
    t = user.query.filter_by(id=4444).first()
    assert t.email == 'my_new_email@example.com'
    """
Function for updating the title of a journey
 
    """
def test_update_journey(db_handle): 
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    j = _get_journey()
    db_handle.session.add(j)
    db_handle.session.commit()
    journey.query.filter_by(id=5555).update(dict(title='My new title'))
    t = journey.query.filter_by(id=5555).first()
    assert t.title == 'My new title'

def test_update_day(db_handle): 
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    j = _get_journey()
    db_handle.session.add(j)
    db_handle.session.commit()
    d = _get_day()
    db_handle.session.add(d)
    db_handle.session.commit()
    day.query.filter_by(id=6666).update(dict(description='My new description'))
    t = day.query.filter_by(id=6666).first()
    assert t.description == 'My new description'
 
 
def test_user_columns(db_handle):
    """
    Tests sensor columns' restrictions. Name must be unique, and name and model
    must be mandatory.
    """

    user_1 = _get_user()
    user_2 = _get_user()
    db_handle.session.add(user_1)
    db_handle.session.add(user_2)    
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

def test_error_journey(db_handle):
    db_handle.session.add(_get_journey())
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_error_day(db_handle):
    db_handle.session.add(_get_day())
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_error_image(db_handle):
    db_handle.session.add(_get_image())
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
        
