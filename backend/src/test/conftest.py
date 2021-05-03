import os
import unittest
from flask import Flask
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime,ARRAY,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
from sqlalchemy.orm.attributes import QueryableAttribute

 
#from backend.app import app 
#from entities.database import database
 
TEST_DB = 'test.db'
engine = create_engine("mssql+pyodbc://IND-CHN-LT10861\SQLEXPRESS/master?driver=SQL Server?Trusted_Connection=yes")
Session = sessionmaker(bind=engine)
Base = declarative_base()

 
class BasicTests(unittest.TestCase):
 
# executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

# executed after each test
    def tearDown(self):
        pass
    

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
if __name__ == "__main__":
    unittest.main()

"""
import os
import tempfile

import pytest

from flask import Flask


@pytest.fixture
def client():
    db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
    flask.app.config['TESTING'] = True

    with flask.app.test_client() as client:
        with flask.app.app_context():
            flask.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flask.app.config['DATABASE'])
"""    