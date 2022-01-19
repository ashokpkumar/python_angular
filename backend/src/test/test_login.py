import pytest
from flask import Flask
import requests 
app = Flask(__name__)
app.testing = True 
#Base.metadata.create_all(engine) 
c = app.test_client()
c.get('http://localhost:5000/login').data
#from entities.sample_data import create_sample_employee,create_sample_project,create_sample_timesubmissions,create_sample_authUser,time_master
#from collections.abc import Iterable
def test_set_password():
    pass

def test_login():
    url='http://localhost:5000/login'
    data = {"emp_id":"Manager","password":"manager123"}
    resp = c.get(url,json=data)
    assert resp.status_code==200
    assert resp.data == json