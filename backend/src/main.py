#from .entities.entity import Session, engine, Base

# sources
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
#https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47#:~:text=To%20add%20a%20serialization%20method,columns%20and%20returns%20a%20dictionary.&text=def%20to_dict(self%2C%20show%3D,of%20this%20model.%22%22%22
#sources
import logging
#from entities.exam import Exam,ExamSchema
from urllib import response

from entities.database import employee,project,authUser,timesubmissions
from entities.database import Session, engine, Base
from entities.database import serialize_all
from entities.sample_data import create_sample_employee,create_sample_project,time_master
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
# create_sample_employee()
# create_sample_project()
# time_master()


@app.route("/setpassword", methods=["POST"])
def setpassword():
    logging.info("Set password Request")
    session = Session()
    if request.json.get("emp_id") is None:
        logging.error("setpassword:: emp_id is a required field")
        response.status = 400
        return response.write({
            "status": "error",
            "message": "emp_id is required field"
        })

    if request.json.get("password") is None:
        logging.error("setpassword:: password is a required field")
        self.response.status = 400
        return self.response.write({
            "status": "error",
            "message": "password is required field"
        })
    emp_id = request.json.get("emp_id")
    password = request.json.get("password")
    try:
        auth_object = session.query(authUser).filter(authUser.emp_id == emp_id).first()
        if auth_object is None:
            return jsonify({'error': 'User not found, This user is not added yet'}), 200
    except:
        return jsonify({'error': 'User not found, This user is not added yet'}), 400
    try:
        auth_object.password =password
        session.add(auth_object)
        session.commit()
        session.close()
        return jsonify({'success': 'password set successfully ! Please login with your new password'}), 200
    except:
        return jsonify({'error': 'Unable to reset password'}), 400


@app.route("/login", methods=["POST"])
def login():
    if request.json.get("emp_id") and request.json.get("password") is None:
        logging.error("login:: emp_id and password is a required field")
        response.status = 400
        return response.write({
            "status": "error",
            "message": "emp_id and password is wrong"
        })

    emp_id = request.json.get("emp_id")
    password = request.json.get("password")
    login=False
    if emp_id==None or password==None:
        return jsonify({"error:":"incorrect username or password"}), 200

    try:
        session = Session()
        auth_object = session.query(authUser).filter(authUser.emp_id == emp_id).first()
        if auth_object and auth_object.password==None:
                return jsonify({"warning":"Password Not set Please set password"}), 200

        auth_object = session.query(authUser).filter(authUser.emp_id == emp_id, authUser.password == password).first()
        if auth_object==None:
            return jsonify({"error":"Username or password is incorrect"}), 200
        emp_obj = session.query(employee).filter(employee.emp_id == emp_id).first()
        employee_name = emp_obj.salutation + " " + emp_obj.first_name + " " + emp_obj.last_name
        roles=auth_object.roles
        login=True
        access_token = create_access_token(identity=emp_id)
        return jsonify(access_token=access_token,username=emp_id,roles=roles,login=login,employee_name = employee_name)
    except:
        return jsonify({"error": "Username or password is incorrect"}), 400


@app.route('/timesubmissions')
# @jwt_required()
def timesubmission():
    try:
        session = Session()
        sub_objects = session.query(timesubmissions).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return jsonify(serialized_obj)
    except:
        return jsonify({"error": "Unable to connect with DB"}), 400


@app.route('/employees')
# @jwt_required()
def employees():
    try:
        session = Session()
        emp_objects = session.query(employee).all()
        serialized_obj = serialize_all(emp_objects)
        #serialized_obj = [{"title":obj.title,"description":obj.description} for obj in emp_objects]
        session.close()
        return jsonify(serialized_obj)
    except:
        return jsonify({"error": "Unable to connect with DB"}), 400


@app.route('/projects')
# @jwt_required()
def projects():
    try:
        session = Session()
        project_objects = session.query(project).all()
        serialized_obj = serialize_all(project_objects)
        # serialized_obj = [{"project_id":obj.project_id,
        #                     "project_title":obj.project_title,
        #                     "project_start_date":obj.project_start_date,
        #                     "project_status":obj.project_status} for obj in project_objects]
        session.close()
        return jsonify(serialized_obj)
    except:
        return jsonify({"error": "Unable to query from DB. please check DB connection"}), 400


@app.route('/addtimesubmissions', methods=['POST'])
#@jwt_required()
def addtimesubmissions():
    data = request.get_json()
    print(data)
    sub_data = timesubmissions( from_date = datetime.datetime.now(),
                                    to_date = datetime.datetime.now(),
                                    user_name = data.get('user_name'),
                                    manager_name = data.get('manager_name'),
                                    time_type = data.get('time_type'),
                                    status = 'submitted-pending approval',
                                    submission_id = data.get('from_date')
                                                    + data.get('to_date')
                                                    + data.get('user_name')
                                                    + data.get('manager_name')
                                                    + data.get('time_type'),
                               )
    try:
        session = Session()
        session.add(sub_data)
        session.commit()
        return jsonify({'msg':'success'}),200
    except:
        return jsonify({"error": "Unable to query from DB. please check DB connection"}), 400


@app.route('/view_submissions', methods=['POST'])
#@jwt_required()
def view_submissions():
    try:
        session = Session()
        data = request.get_json()
        manager_name = data.get("user_name")
        print(data)

        existing_submissions = session.query(timesubmissions).filter(timesubmissions.manager_name==manager_name).all()
        if existing_submissions:
            serialized_obj = serialize_all(existing_submissions)
            return jsonify(serialized_obj),200
        return jsonify({'info':'No submission available for you'}),200
    except:
        return jsonify({"error": "Unable to query from DB. please check DB connection"}), 400


@app.route('/addEmployee', methods=['POST'])
# @jwt_required()
def addEmployee():
    data = request.get_json()
    session = Session()
    existing_emp = session.query(employee).filter(employee.emp_id==data.get("emp_id")).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'User ID: {} already exist !'.format(data.get("emp_id"))})

    existing_emp = session.query(employee).filter(employee.email==data.get("email")).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'Email ID: {} already exist !'.format(data.get("email"))})

    try:
        emp_data = employee(emp_id=data.get("emp_id") ,
                            email = data.get("email") ,
                            first_name = data.get("first_name"),
                            last_name= data.get("last_name"),
                            sur_name= data.get("sur_name"),
                            initial= data.get("initial"),
                            salutation= data.get("salutation"),
                            project_code= data.get("project_code"),
                            dept= data.get("dept"),
                            designation = data.get("designation"),
                            emp_start_date= datetime.datetime.now(),
                            emp_last_working_date=datetime.datetime.now(),
                            emp_project_assigned_date=datetime.datetime.now(),
                            emp_project_end_date=datetime.datetime.now(),

                            employment_status=data.get("employment_status"),
                            manager_name=data.get("manager_name"),
                            manager_dept=data.get("manager_dept"),
                            resource_status=data.get("resource_status"),
                            delivery_type=data.get("delivery_type"),
                            additional_allocation=data.get("additional_allocation"),
                            skills=data.get("skills"),
                            roles=data.get("roles"),

                            )
        try:
            session = Session()
            session.add(emp_data)
            session.commit()
            auth_data = authUser(emp_id = data.get("emp_id"),
                                email=data.get("email"),
                                roles=data.get("roles"))
            session = Session()
            session.add(auth_data)
            session.commit()
            return jsonify({"success":"successfully added employee {}".format(data.get("emp_id"))}),200
        except:
            return jsonify({"error": "Unable to Add employee. please check emp_id, email and roles"}), 400
    except:
        return jsonify({"error":"Some error happened in adding the employee"}),500


@app.route('/addProjectResource', methods=['POST'])
# @jwt_required()
def addProjectResource():
    session = Session()
    data = request.get_json()
    if request.json.get("emp_id") and request.json.get("project_id") is None:
        logging.error("login:: emp_id and project_id is a required field")
        response.status = 400
        return response.write({
            "status": "error",
            "message": "emp_id and project_id wrong"
        })
    resource_id = data.get("emp_id")
    project_code = data.get("project_id")

    try:
        existing_emp = session.query(employee).filter(employee.emp_id==resource_id).first()
        if existing_emp==None:
            return jsonify({'success':'Employee with ID: {} Does not Exist !'.format(resource_id)})

        existing_project = session.query(project).filter(project.project_code==project_code).first()
        if existing_project==None:
            return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})

        existing_emp.project_code=project_code
        session.add(existing_emp)
        session.commit()
    except:
        return jsonify({"error": "Unable to query from DB. please check DB connection"}), 400
    try:
        if existing_project.resource_info == None:
            existing_project.resource_info=resource_id
            session.add(existing_project)
            session.commit()

        else:
            existing_resource = existing_project.resource_info
            existing_resource_list = existing_resource.split(",")
            for i in existing_resource_list:
                if i=="":
                    existing_resource_list.remove(i)
            if resource_id in existing_resource_list:
                return jsonify({'error':'resource exist already in the project'})
            existing_resource_list.append(resource_id )

            out_resource =''
            for i in existing_resource_list:
                out_resource = i + "," + out_resource
            existing_project.resource_info = out_resource[:-1]
            session.add(existing_project)
            session.commit()

        session.close()
        return jsonify({"success":"Employee {} and Project {} Linked".format(resource_id,project_code)})
    except:
        return jsonify({"error": "Unable to query from DB. please check DB connection"}), 400


@app.route('/addProject', methods=['POST'])
# @jwt_required()
def addProject():
    data = request.get_json()
    session = Session()
    existing_project = session.query(project).filter(project.project_code==data.get("projectcode")).first()
    if existing_project:
        session.close()
        return jsonify({'warning':'Project with ID: {} already exist !'.format(data.get("projectcode"))})
    try:
        project_data = project(client_name = data.get("clientname"),
                                project_code=data.get("projectcode"),
                                project_name=data.get("projectname"),
                                project_start_date=datetime.datetime.now(),
                                project_status=data.get("projectstatus"),
                                billing_type=data.get("billingtype"),
                                segment=data.get("segment"),
                                geography=data.get("geography"),
                                solution_category =data.get("solutioncategory"),
                                financial_year = data.get("financialyear")

        )
        session = Session()
        session.add(project_data)
        session.commit()
        session.close()
        return jsonify({"success":"added data to the table successfully"}), 201
    except:
        return jsonify({"error":"Something happened while adding the data to the table, please check the data and try again"}), 500


if __name__ == '__main__':
    #app.run(host = '0.0.0.0',port = 5000,debug = True)
    app.run(debug = True)
