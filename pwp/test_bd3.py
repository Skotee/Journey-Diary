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

def _get_user():
    return user(
        id = 4444,
        username ="Maella",
        password = "mmmm" ,
        email ="maella.gheraia@gmail.com"
    )

def _get_journey():
    return journey(
        id = 5555,
        user_id = 4444,
        title ="Journey test"
    )

def _get_day():
    return day(
        id = 6666,
        journey_id = 5555,
        date = datetime.now() ,
        description ="Nice trip"
    )

def _get_image():
    return image(
        id = 7777,
        day_id = 6666,
        extension = "jpg" 
    )

def test_create_user(db_handle):
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    assert user.query.count() == 1

def test_delete_user(db_handle):
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.delete(u)
    assert user.query.count() == 0

def test_create_journey(db_handle):
    j = _get_journey()
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    assert journey.query.count() == 1

def test_delete_journey(db_handle):
    j = _get_journey()
    u = _get_user()
    db_handle.session.add(u)
    db_handle.session.commit()
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.delete(j)
    assert journey.query.count() == 0

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
