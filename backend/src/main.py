#from .entities.entity import Session, engine, Base

# sources
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
#https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47#:~:text=To%20add%20a%20serialization%20method,columns%20and%20returns%20a%20dictionary.&text=def%20to_dict(self%2C%20show%3D,of%20this%20model.%22%22%22
#sources

#from entities.exam import Exam,ExamSchema
from entities.database import employee,project,authUser
from entities.database import Session, engine, Base
from entities.database import serialize_all
from entities.sample_data import create_sample_employee,create_sample_project

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import time
import datetime
from sqlalchemy.ext.serializer import loads, dumps

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
CORS(app)


# generate database schema
Base.metadata.create_all(engine)
create_sample_employee()
create_sample_project()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    print(username)
    print(password)
    if username==None or password==None:
        return jsonify({"error:":"incorrect username or password"}), 500

    session = Session()
    auth_object = session.query(authUser).filter(authUser.username == username, authUser.password == password).first()
    print(auth_object)
    if not auth_object:
        return jsonify({"error":"Username or password is incorrect"}), 400
    
    # if username != "test" or password != "test":
    #     return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/employees')
@jwt_required()
def employees():
    session = Session()
    emp_objects = session.query(employee).all()
    serialized_obj = serialize_all(emp_objects)
    #serialized_obj = [{"title":obj.title,"description":obj.description} for obj in emp_objects]
    session.close()
    return (jsonify(serialized_obj))


@app.route('/projects')
@jwt_required()
def projects():
    session = Session()
    project_objects = session.query(project).all()
    serialized_obj = serialize_all(project_objects)
    # serialized_obj = [{"project_id":obj.project_id,
    #                     "project_title":obj.project_title,
    #                     "project_start_date":obj.project_start_date,
    #                     "project_status":obj.project_status} for obj in project_objects]
    session.close()
    return (jsonify(serialized_obj))


@app.route('/addEmployee', methods=['POST'])
@jwt_required()
def addEmployee():
    data = request.get_json()
    emp_data = employee(first_name=data["first_name"] , 
                        last_name = data["last_name"], 
                        sur_name= data["sur_name"], 
                        initial= data["initial"], 
                        salutation= data["salutation"], 
                        project_id= data["project_id"], 
                        dept= data["dept"], 

                        emp_start_date= datetime.datetime.now(),
                        emp_last_working_date=datetime.datetime.now(),
                        emp_project_assigned_date=datetime.datetime.now(),
                        emp_project_end_date=datetime.datetime.now(),

                        employment_status=data["employment_status"], 
                        manager_name=data["manager_name"], 
                        manager_dept=data["manager_dept"], 

                        )
    session = Session()
    session.add(emp_data)
    session.commit()
    emp_data.to_dict()
    return jsonify(emp_data.to_dict()), 201


@app.route('/addProject', methods=['POST'])
@jwt_required()
def addProject():
    data = request.get_json()
    project_data = project(project_id=data["project_id"] , 
                        project_title = data["project_title"], 
                        project_start_date= datetime.datetime.now(),
                        project_status= data["status"],    
                        )
    session = Session()
    session.add(project_data)
    session.commit()
    project_data.to_dict()
    return jsonify(project_data.to_dict()), 201

@app.route('/resource_info', methods=['POST'])
@jwt_required()
def resource_info():
    data = request.get_json()
    project_data = project(project_id=data["project_id"] , 
                        emp_id = data["emp_id"], 
                        )
    session = Session()
    session.add(project_data)
    session.commit()
    project_data.to_dict()
    return jsonify(project_data.to_dict()), 201


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5000,debug = True)