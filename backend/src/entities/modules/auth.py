from flask import Blueprint, json, jsonify, request
#from src.entities.schema_manager import switchSchema,getsession
from entities.database import  serialize_all, authUser
from datetime import datetime
import datetime
# from sqlalchemy import or_
#from cryptography.fernet import Fernet
from env.config import Config
import json
import jwt
import logging
auth_module = Blueprint(name="auth", import_name=__name__)


def jwtvalidate(func):
    def jswdecode():
        bearer_token =request.headers.get('Authorization',None)
        emp_id =request.headers.get('X-TenantID',None)
        print(bearer_token)
        logging.info(bearer_token)
        print(logging.info(bearer_token))
        logging.info(emp_id)
        logging.log(1,bearer_token)
        logging.log(1,emp_id)
        print(bearer_token)
        print(emp_id)
        if bearer_token==None or emp_id==None:
            return jsonify({"error":"JWT Failed: Required auth parameter missing{}{}".format(bearer_token,emp_id)}),400
        bearer_token = bearer_token.split(" ")[1]

        try:
            payload = jwt.decode(bearer_token, Config.JWT_SECRET_KEY,algorithms='HS256')
            # print("payload",payload)
            #user_id = payload["username"]
            token_emp_id = payload["emp_id"]
            roles = payload["roles"]

            if token_emp_id!=emp_id:
                return jsonify({"error":"Incorrect Employee ID"}),400

            session = switchSchema("public")
            emp_exist = session.query(employee).filter(employee.emp_id==token_emp_id).all()
            if emp_exist==None or emp_exist == []:
                return jsonify({"error":"Employee with ID: {} does not exist".format(token_emp_id)}),400

            user_info = serialize_all(emp_exist)[0]
            # print("token_client_id",token_client_id)
            session = switchSchema(token_emp_id)
            # user_exist = session.query(User).filter(User.userid==user_id).all()
            # # print("user_exist",user_exist)

            # if user_exist==None or user_exist ==[]:
            #     return jsonify({"error":"User with ID: {}  not exist".format(user_id)}),400

            # user_exist = serialize_all(user_exist)[0]
      
            res = {**user_info}
       
            return func()        
        except jwt.ExpiredSignatureError:
            return jsonify({"error":"Signature expired. Please log in again."}),400

        except jwt.InvalidTokenError:
            return jsonify({"error",'Invalid token. Please log in again.'}),400


    jswdecode.__name__ = func.__name__
    return jswdecode


# def adminrequired(func):
#     def checkadmin():
#         bearer_token =request.headers.get('Authorization',None)
#         client_id =request.headers.get('X-TenantID',None)
#         logging.info(bearer_token)
#         logging.log(1,bearer_token)
#         logging.log(1,client_id)
#         logging.info(client_id)
#         if bearer_token==None or client_id==None:
#             return jsonify({"error":"ADMIN required Failed: Required auth parameter missing{}{}".format(bearer_token,client_id)}),400
#         bearer_token = bearer_token.split(" ")[1]

#         try:
#             payload = jwt.decode(bearer_token, Config.JWT_SECRET_KEY,algorithms='HS256')
#             user_id = payload["username"]
#             token_client_id = payload["client_id"]

#             if token_client_id!=client_id:
#                 return jsonify({"error":"Incorrect Client error"}),400

#             session = switchSchema("public")
#             client_exist = session.query(Clients).filter(Clients.client_id==token_client_id).all()
#             if client_exist==None or client_exist == []:
#                 return jsonify({"error":"Client with ID: {} does not exist".format(token_client_id)}),400

#             user_info = serialize_all(client_exist)[0]
        
#             session = switchSchema(token_client_id)
#             user_exist = session.query(User).filter(User.userid==user_id).all()

#             if user_exist==None or user_exist ==[]:
#                 return jsonify({"error":"User with ID: {} does not exist".format(user_id)}),400

#             user_exist = serialize_all(user_exist)[0]
#             # print(user_exist)
#             # print(user_exist["roles"])
#             user_roles = convert_str_array_to_list(user_exist["roles"])

#             if not "admin" in user_roles:
#                 return jsonify({"error":"Admin rights missing to perform the operation"}),400
#             return func()   
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error":"Signature expired. Please log in again."}),400

#         except jwt.InvalidTokenError:
#             return jsonify({"error":"Invalid token. Please log in again."}),400
#     checkadmin.__name__ = func.__name__
#     return checkadmin