from flask import Blueprint, json, jsonify, request
from entities.database import  serialize_all, authUser
import datetime
from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions,department,designation
from entities.database import Session
from entities.helper import listToString
from env.config import Config
import json
import jwt
import logging

auth_module = Blueprint(name="auth", import_name=__name__)

def jwtvalidate(func):
    def jswdecode():
        # try:
        session = Session()
        bearer_token =request.headers.get('Authorization',None)
        logging.info(bearer_token)
        print(bearer_token,">>>>>>")
        logging.log(1,bearer_token)
        if bearer_token==None:
            return jsonify({"error":"JWT Failed: Required auth parameter missing{}".format(bearer_token)})
        
        bearer_token = bearer_token.split(" ")[1]
        payload = jwt.decode(bearer_token,"super-secret",algorithms='HS256')
        user_id = payload["emp_id"]
        print(user_id,"User_Id>>>>>>")
        
        user_exist = session.query(authUser).filter(authUser.emp_id==user_id).all()


        if user_exist==None or user_exist ==[]:
            return jsonify({"error":"User with ID: {}  not exist".format(user_id)}),400

        user_exist = serialize_all(user_exist)[0]
        print(user_exist,"res")
        res = {**user_exist}
        print(res,"res")
        return func(res)

        # except jwt.ExpiredSignatureError:
        #     return jsonify({"error":"Signature expired. Please log in again."}),400

        # except jwt.InvalidTokenError:
        #     return jsonify({"error",'Invalid token. Please log in again.'}),400

    jswdecode.__name__ = func.__name__
    return jswdecode




