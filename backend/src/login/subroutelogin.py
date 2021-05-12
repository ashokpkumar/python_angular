from flask import Blueprint
from flask import Flask, jsonify, request

from entities.database import authUser,employee
from entities.database import Session
from flask_jwt_extended import create_access_token

login_bp = Blueprint("login_bp",__name__)

@login_bp.route("/login")
def login():
    emp_id = request.json.get("emp_id", None)
    password = request.json.get("password", None)
    login=False
    if emp_id==None or password==None:
        return jsonify({"error:":"incorrect username or password"}), 200
    session = Session()
    # we can use both emp_id and email as a user id.
    if emp_id.find("@") != -1:
        auth_object = session.query(authUser).filter(authUser.email == emp_id, authUser.password == password).first()
    else:
        auth_object = session.query(authUser).filter(authUser.emp_id == emp_id, authUser.password == password).first()

    if auth_object and auth_object.password==None:
        return jsonify({"warning": "Password Not set Please set password"}), 200

    if auth_object is None:
        return jsonify({"error": "Username or password is incorrect"}), 200
    emp_obj = session.query(employee).filter(employee.emp_id == emp_id).first()
    employee_name = "Full Name"
    roles = auth_object.roles
    login=True
    access_token = create_access_token(identity=emp_id)
    return jsonify(access_token=access_token, username=emp_id, roles=roles, login=login, employee_name=employee_name)

