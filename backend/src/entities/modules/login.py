from flask import Blueprint, jsonify, request
import datetime
from env.config import Config 
from flask import request, render_template
#from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
from flask_expects_json import expects_json
from flask_mail import Mail, Message
from entities.modules.auth import jwtvalidate
from entities.helper import hash_password
import json
import jwt
import logging


from flask_mail import Mail, Message

from entities.database import employee,project,authUser,timesubmissions, forget_pass
from entities.database import Session,serialize_all

from env.config import Config

login_module = Blueprint(name="login", import_name=__name__)


@login_module.route("/setpassword", methods=["POST"])
def setpassword():
    session = Session()
    emp_id = request.json.get("emp_id", None)
    password = request.json.get("password", None)
    auth_object = session.query(authUser).filter(authUser.emp_id == emp_id).first()
    if auth_object is None:
        return jsonify({'error':'User not found, This user is not added yet'}),400
    auth_object.password=hash_password(password)
    session.add(auth_object)
    session.commit()
    session.close()
    return jsonify({'success':'password set successfully ! Please login with your new password'}),200


@login_module.route("/login", methods=["POST"])
def login():
    emp_id = request.json.get("emp_id", None)
    password = request.json.get("password", None)
    hashed=hash_password(password)
    login=False
    if emp_id==None or password==None:
        return jsonify({"error:":"incorrect username or password"}),400
    session = Session()
    # we can use both emp_id and email as a user id.
    if emp_id.find("@") != -1:
        auth_object = session.query(authUser).filter(authUser.email == emp_id, authUser.password == hash_password(password)).first()
        emp_obj = session.query(employee).filter(employee.email == emp_id).first()
        employee_name =(emp_obj.first_name if emp_obj.first_name else "")
        emp_id=(emp_obj.emp_id)

    else:
        auth_object = session.query(authUser).filter(authUser.emp_id == emp_id, authUser.password == hash_password(password)).first()
        emp_obj = session.query(employee).filter(employee.emp_id == emp_id).first()
        employee_name =(emp_obj.first_name if emp_obj.first_name else "")
        

    if auth_object and auth_object.password==None:
        return jsonify({"warning": "Password Not set Please set password"}),400

    if auth_object is None:
        return jsonify({"error": "Username or password is incorrect"}),400
    # emp_obj = session.query(employee).filter(employee.emp_id == emp_id).first()
    # employee_name =(emp_obj.first_name if emp_obj.first_name else "")
    # employee_name = (emp_obj.first_name if emp_obj.first_name else "") + (emp_obj.last_name if emp_obj.last_name else "")
    roles = auth_object.roles

    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=Config.AUTH_TOKEN_EXPIRY_DAYS, seconds=Config.AUTH_TOKEN_EXPIRY_SECS),
            'iat': datetime.datetime.utcnow(),
            'emp_id': emp_id,
            'roles':roles
            # 'username':input_user_id
        }

        jwt_info = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        print(jwt_info)
        login=True
        return jsonify(access_token=jwt_info,username=emp_id,roles=roles,login=login,employee_name = employee_name),200

    except Exception as e:
        return e
    # login=True
    # access_token = create_access_token(identity=emp_id)
    # return jsonify(access_token=access_token,username=emp_id,roles=roles,login=login,employee_name = employee_name)


@login_module.route("/forgot_pass_create_token", methods=["POST"])
def forgot_pass_create_token():
    session = Session()
    email_id = request.json.get("email_id")
    emp_objects = session.query(employee).filter(employee.email == email_id).first()
    if emp_objects == None:
        return jsonify({"error":" Please enter Valid employee Email Id"}),400

    emp_id = emp_objects.emp_id
    forget_pass_data = session.query(forget_pass).filter(forget_pass.user_id == emp_id,
                                                         forget_pass.email_address == email_id,
                                                         ).first()
    access_token = create_access_token(identity=emp_id)
    current_date = datetime.datetime.now()

    if forget_pass_data == None:
        forget_pass_obj = forget_pass(user_id=emp_id, email_address=email_id, reset_token=access_token, create_date=current_date)
        session.add(forget_pass_obj)
        session.commit()
        session.close()

    else:
        forget_pass_data.reset_token = access_token
        forget_pass_data.create_data = current_date
        session.add(forget_pass_data)
        session.commit()
        session.close()

        html_body = render_template('frontend/frontend/src/app/reset-password/reset-password.component.html',
                                    user=email_id, token=access_token)
        text_body = "http://localhost:4200/" + 'resetpassword/?token='+access_token +'&'+'email='+email_id
        send_mail("Forgot password setup", Config.MAIL_USERNAME, email_id, html_body, text_body)

        return jsonify(text_body),200


@login_module.route("/reset_pass", methods=["POST", "GET"])
def reset_pass():
    session = Session()
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_pass = request.json.get('password')
    token = request.json.get('reset_token')

    if email is None:
        return jsonify({"error:": "incorrect username or password"}), 400

    forget_pass_objects = session.query(forget_pass).filter(forget_pass.email_address == email)
    forget_pass_obj = serialize_all(forget_pass_objects)

    reset_token = forget_pass_obj[0]['reset_token']
    if reset_token == token:
        # update auth table password
        auth_object = session.query(authUser).filter(authUser.email == email).first()
        if auth_object is None:
            return jsonify({'error': 'User not found, This user is not added yet'}), 400
        auth_object.password = hash_password(password)
        session.add(auth_object)
        session.commit()
        session.close()

        return "Password Reset successfully", 200
    else:
        return "Please generate token for reset password  token expired", 400


def send_mail(subject, sender, recipients, body, html_body):
   msg = Message(subject=subject, sender=sender, recipients=[recipients])
   msg.html = html_body
   msg.body = body
   mail.send(msg)