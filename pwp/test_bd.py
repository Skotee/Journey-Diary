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
    db_handle.session.add(_get_user())
    db_handle.session.add(_get_journey())
    db_handle.session.commit()
    assert journey.query.count() == 1

def test_delete_journey(db_handle):
    j = _get_journey()
    db_handle.session.add(_get_user())
    db_handle.session.add(j)
    db_handle.session.commit()
    db_handle.session.delete(j)
    assert journey.query.count() == 0

