#from .entities.entity import Session, engine, Base
# sources
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
#https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47#:~:text=To%20add%20a%20serialization%20method,columns%20and%20returns%20a%20dictionary.&text=def%20to_dict(self%2C%20show%3D,of%20this%20model.%22%22%22
#sources

from entities.database import employee,project,authUser,timesubmissions,TimeMaster, forget_pass
from entities.database import employee,project,authUser,timesubmissions
from entities.database import announcements
from entities.database import Session, engine, Base
from entities.database import serialize_all
from entities.sample_data import create_sample_employee,create_sample_project,create_sample_timesubmissions,create_sample_authUser,time_master
from entities.helper import helper1,helper2,removenull

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_expects_json import expects_json
from flask_mail import Mail, Message

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import time
import datetime
import json
import pytest
from sqlalchemy.ext.serializer import loads, dumps
import entities.mail
from flask import request, render_template
import os
from env.config import Config


template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
app = Flask(__name__, template_folder=template_dir)
app.config.from_object(Config)
mail = Mail(app)


# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
CORS(app)


Base.metadata.create_all(engine)
time_master()
create_sample_employee()
create_sample_project()
create_sample_timesubmissions()
create_sample_authUser()


@app.route("/setpassword", methods=["POST"])
def setpassword():
    session = Session()
    emp_id = request.json.get("emp_id", None)
    password = request.json.get("password", None)
    auth_object = session.query(authUser).filter(authUser.emp_id == emp_id).first()
    if auth_object is None:
        return jsonify({'error':'User not found, This user is not added yet'}), 200
    auth_object.password=password
    session.add(auth_object)
    session.commit()
    session.close()
    return jsonify({'success':'password set successfully ! Please login with your new password'}),200

@app.route("/login", methods=["POST"])
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
    return jsonify(access_token=access_token,username=emp_id,roles=roles,login=login,employee_name = employee_name)


@app.route('/employees')
def employees():
    session = Session()
    emp_objects = session.query(employee).all()
    serialized_obj = serialize_all(emp_objects)
    serialed_out = []
    for dictionary in serialized_obj:
        dictionary['full_name'] = dictionary['first_name'] + dictionary['last_name']
        serialed_out.append(dictionary)

    project_objects = session.query(project).all()
    serialized_project = serialize_all(project_objects)
    for dictionary in serialed_out:
        emp_id = dictionary["project_code"]
        for proj_item in serialized_project:
            if proj_item["project_code"]==emp_id:
                proj_item["project_code"] = [emp_id] #Project id should return list instead of string in employee
                dictionary.update(proj_item)
                break
    session.close()
    return (jsonify(serialed_out))


@app.route('/events')
def events():
    session = Session()
    time_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(time_objects)
    events_data = []
    for event in serialized_obj:
        eve={}
        eve["title"]="*" + str(event["time_type"]) + " : "+ str(event["hours"]) + " Hours"
        eve["start"]=event["date_info"]
        events_data.append(eve)   
    return jsonify(events_data)

@app.route('/announcements')
def announcement():
    session = Session()
    announcement_objects = session.query(announcements).all()
    serialized_obj = serialize_all(announcement_objects)
    session.close()
    return (jsonify(serialized_obj))


@app.route('/projects')
def projects():
    session = Session()
    project_objects = session.query(project).all()
    serialized_obj = serialize_all(project_objects)
    session.close()
    return (jsonify(serialized_obj))

@app.route('/add_announcements', methods=['POST'])
def add_announcements():
    data = request.get_json()
    announcement_data = announcements (user_id =data.get('user_id'),
                                       announcement_info = data.get('announcement_info'),
                                       announcement_category=data.get('announcement_category'),
                                       date_logged = datetime.datetime.now(),
                                        )
    session = Session()
    session.add(announcement_data)
    session.commit()    
    return ({'success':'Announcements are added sucessfully '})

@app.route('/get_announcements', methods=['POST'])
def get_announcements():
    session = Session()
    data = request.get_json()
    user_id = data.get("user_id")
    existing_announcements = session.query(announcements).filter(announcements.user_id==user_id).order_by(announcements.id.desc())[-30:]
    if existing_announcements:
    #ann = announcements.select([announcements]).order_by(-announcements.c.id.desc()).limit(2)
    #if ann:
        serialized_obj = serialize_all(existing_announcements)
        print(serialized_obj)
        return jsonify(serialized_obj),200  
    return jsonify({'info':'No announcements are available for you'}),200

@app.route('/del_fn',methods=['POST'])
def delete_fn():
    session = Session()
    data = request.get_json()
    x = data.get("x")
    delete_announcements=session.query(announcements).filter(announcements.id>=x).delete()
    #delete_announcements = announcements.delete().where(announcements.c.id > x)
    return jsonify({'info':'announcements are deleted '}),200



@app.route('/addtimesubmissions', methods=['POST'])
def addtimesubmissions():    
    data = request.get_json() 
    user_id = data.get('user_name')
    session = Session()
    existing_emp = session.query(employee).filter(employee.emp_id == user_id ).first()
    if existing_emp == None:
        return jsonify({'error':'user not available in the employee table'}),200
    sub_data = timesubmissions( date_info = data.get('date'),
                                    hours = data.get('hours'),
                                    user_id = data.get('user_name'),
                                    project_code = data.get('project_id'),
                                    manager_id = data.get('manager_name'),
                                    time_type = data.get('time_type'),
                                    status = 'submitted-pending approval',
                                    submission_id = data.get('user_name') + data.get('user_name') + data.get('time_type')     
                               )
    session = Session()
    session.add(sub_data)
    session.commit()
    return jsonify({'success':'Your Time has been  submitted for: {}'.format(data.get('date'))}),200


@app.route('/view_submissions', methods=['POST'])
def viewsubmissions():
    session = Session()
    data = request.get_json()
    manager_name = data  
    print(manager_name)
    emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_name).all()
    emp_final = [emp[0].lower() for emp in emp_list]
    print(emp_final)
    submission_obj = session.query(timesubmissions).filter(timesubmissions.manager_id.in_(emp_final),timesubmissions.status=='submitted-pending approval' ).all()
    print(submission_obj)
    if submission_obj:
        serialized_obj = serialize_all(submission_obj)
        print(serialized_obj)
        return jsonify(serialized_obj),200
    return jsonify({'info':'No submission available for you'}),200
  

@app.route('/timesubmissions')
def timesubmission():
    session = Session()
    sub_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(sub_objects)
    session.close()
    return (jsonify(serialized_obj))

@app.route('/getSubmissionsBy', methods=['POST'])
def getSubmissionsBy():
    session = Session()
    user = request.get_json()
    if user == 'total':
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='submitted-pending approval').all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200
        
    else:
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='submitted-pending approval', timesubmissions.user_id==user).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200


@app.route('/getTimeBy', methods=['POST'])
def getTimeBy():
    session = Session()
    data = request.get_json()
    time_type = data['type']
    user = data['user']
    print(user)
    print(time_type)
    if user == 'total':
        if time_type =="project":
            time_type_list = ['wfh','REG']
        else:
            time_type_list = [time_type]
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='approved',timesubmissions.time_type.in_(time_type_list)).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200
        
    else:
        if time_type =="project":
            time_type_list = ['wfh','REG']
        else:
            time_type_list = [time_type]
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='approved',timesubmissions.time_type.in_(time_type_list),timesubmissions.user_id==user).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200
           

@app.route('/timeData', methods=['POST'])
def timeData():
    manager_id = request.get_json()
    session = Session()
    emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
    emp_final = [emp[0].lower() for emp in emp_list]
    time_final = []
    for emp in emp_final:
        project_time = 0
        sl = 0
        cl=0
        al=0
        bench=0
        user_id = emp
        unapproved=0

        user_name = session.query(employee.first_name).filter(employee.emp_id==emp).first()[0]
        submission_obj = session.query(timesubmissions).filter(timesubmissions.manager_id.in_(emp_final), timesubmissions.user_id==emp).all()
        serialized_obj = serialize_all(submission_obj)
        for time in serialized_obj:
            #print(time)
            if time['status']=='approved':
                if time['time_type']=='wfh' or time['time_type']=='REG':
                    project_time = project_time + time['hours']
                elif time['time_type']=='sl':
                    sl = sl + time['hours']
                elif time['time_type']=='cl':
                    cl = cl + time['hours']
                elif time['time_type']=='al':
                    al = al + time['hours']
                elif time['time_type']=='bench':
                    bench = bench + time['hours']
            else:
                unapproved = unapproved + time['hours']    
        
        total_hrs = project_time + sl + cl + al + bench
        time_final.append({'user_id':user_id, 'user_name': user_name, 'project_time':project_time,'sl':sl,'cl':cl,'al':al,'bench':bench,'unapproved':unapproved, 'total_hrs':total_hrs})
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(time_final)  
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    total_project = 0
    total_sl = 0
    total_cl = 0
    total_al = 0
    total_bench = 0
    total_unapproved = 0

    for emp_data in time_final:
        total_project = total_project  + emp_data['project_time']
        total_sl = total_sl  + emp_data['sl']
        total_cl = total_cl  + emp_data['cl']
        total_al = total_al  + emp_data['al']
        total_bench = total_bench  + emp_data['bench']
        total_unapproved = total_unapproved + emp_data['unapproved']
    total_time_list = {'total_project':total_project,'total_sl':total_sl,'total_cl':total_cl,'total_al':total_al,'total_bench':total_bench,'total_unapproved':total_unapproved, }
    print(total_time_list)
    #time_final.append({'total_project':total_project,'total_sl':total_sl,'total_cl':total_cl,'total_al':total_al,'total_bench':total_bench,'total_unapproved':total_unapproved, })
    return (jsonify({'result':time_final,'total':total_time_list}))


@app.route('/review_time', methods=['POST'])
def review_time():
    data = request.get_json()
    #print(data)
    if data['reviewd']==True:
        session = Session()
        username = data['user_name']
        date = data['date']
        time_type = data['time_type']
        hours = data['hours']
        datee = datetime.datetime.strptime(date, "%Y-%m-%d")
        month = datee.month
        year = datee.year
        time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours).first()
        time_obj.status = "approved"
        session.add(time_obj)
        session.commit()
        session.close()
        return jsonify({"info":"Time has been reviewed"})
        # username = data['user_name']
        # date = data['date']
        # time_type = data['time_type']
        # hours = data['hours']
        # session = Session()
        # datee = datetime.datetime.strptime(date, "%Y-%m-%d")
        # month = datee.month
        # year = datee.year
        # existing_emp = session.query(TimeMaster).filter(TimeMaster.month==month,TimeMaster.year==year,TimeMaster.emp_id==username).first()
        # if existing_emp:
        #     #month Information has been already added just need to add the date to the month data
        #     timedata = json.loads(existing_emp.timedata)
        #     if date in timedata.keys():
        #         date_info = timedata[date]
        #         print(">>>>>>>>>>>>>>>>>")
        #         print(date_info)
        #         if time_type in date_info.keys():
        #             print("time type already present")
        #             session = Session()
        #             del_obj = session.query(timesubmissions).filter(timesubmissions.date_info==date,timesubmissions.user_id==username,timesubmissions.time_type==time_type,timesubmissions.hours==hours).first()
        #             #session.delete(del_obj)
        #             session.commit()
        #             session.close()
        #             return jsonify({"error":"Info already in the Data"}),200
        #         else:
        #             date_info[time_type]=hours
        #             timedata[date]=date_info
        #             existing_emp.timedata = json.dumps(timedata)
        #             #session = Session()
        #             session.add(existing_emp)
        #             session.commit()
        #             session.close()
        #             return jsonify({"success":"Time has been reviewed"})

        #     else:
        #         timedata[date] = {time_type:hours}
        #         existing_emp.timedata = json.dumps(timedata)
        #         session.add(existing_emp)
        #         session.commit()
        #         session.close()

        #         session = Session()
        #         del_obj = session.query(timesubmissions).filter(timesubmissions.date_info==date,timesubmissions.user_id==username,timesubmissions.time_type==time_type,timesubmissions.hours==hours).first()
        #         #session.delete(del_obj)
        #         session.commit()
        #         session.close()
                
        #         return jsonify({"success":"Time has been reviewed"})
           
        # else:
        #     #month information is not present already. hence create the month information along with the existing data
        #     time_obj = TimeMaster(emp_id = username,
        #                           month = month , 
        #                           year = year,
        #                           timedata = json.dumps({date:{time_type:hours}})
        #         )
        #     session.add(time_obj)
        #     session.commit()
        #     session.close()

        #     session = Session()
        #     del_obj = session.query(timesubmissions).filter(timesubmissions.date_info==date,timesubmissions.user_id==username,timesubmissions.time_type==time_type,timesubmissions.hours==hours).first()
        #     #session.delete(del_obj)
        #     session.commit()
        #     session.close()

        #     return jsonify({"success":"Time has been reviewed"})

    elif data['reviewd']==False:
        session = Session()
        username = data['user_name']
        date = data['date']
        time_type = data['time_type']
        hours = data['hours']
        datee = datetime.datetime.strptime(date, "%Y-%m-%d")
        month = datee.month
        year = datee.year
        time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours).first()
        time_obj.status = "denied"
        session.add(time_obj)
        session.commit()
        session.close()
        return jsonify({"info":"Time has been reviewed"})


schema ={
    "type": "object",
    "properties": {
      "emp_id":{"type":"string"},
      "email": { "type": "string", "format": "email","pattern":"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"},
      "first_name": { "type": "string", "minLength": 2, "maxLength": 50 },
      "last_name": { "type": "string", "minLength": 2, "maxLength": 50 },
      "sur_name": { "type": "string", "minLength": 2, "maxLength": 50 },
      "initial": { "type": "string", "minLength": 2, "maxLength": 4 },
      "salutation": { "type": "string", "minLength": 2,  },
      "project_code": { "type": "string", "minLength": 2, "maxLength": 50 },
      "dept": { "type": "string", "minLength": 2, "maxLength": 50 },
      "designation": { "type": "string", "minLength": 2, "maxLength": 100 },
      "emp_start_date":  { "type": "string","format": "date","pattern":"(0[1-9]|1[0-9]|2[0-9]|3[01]).(0[1-9]|1[012]).[0-9]{4}"},
      "emp_last_date":  { "type": "string","format": "date","pattern":"(0[1-9]|1[0-9]|2[0-9]|3[01]).(0[1-9]|1[012]).[0-9]{4}"},
      "emp_project_assigned_date":  { "type": "string","format": "date","pattern":"(0[1-9]|1[0-9]|2[0-9]|3[01]).(0[1-9]|1[012]).[0-9]{4}"},
      "emp_project_end_date":  { "type": "string","format": "date","pattern":"(0[1-9]|1[0-9]|2[0-9]|3[01]).(0[1-9]|1[012]).[0-9]{4}"},
      "employment_status": { "type": "boolean"},
      "manager_name": { "type": "string", "minLength": 2, "maxLength": 50 },
      "manager_dept": { "type": "string", "minLength": 2, "maxLength": 50 },
      "resource-status": { "type": "string", "minLength": 2, "maxLength": 100 },
      "delivery_type": { "type": "string", "minLength": 2, "maxLength": 50 },
      "additional_allocation": { "type": "string", "minLength": 2, "maxLength": 100 },
      "skills": { "type": "string", "minLength": 2, "maxLength": 100 },
      "roles": { "type": "string", "minLength": 2, "maxLength": 100 },
    },
    "required": [ "emp_id", "email", "first_name","last_name","sur_name","initial","salutation","project_code",
    "dept","designation","emp_last_working_date","emp_project_assigned_date","emp_project_end_date","employment_status",   
    "manager_name","manager_dept","resource_status","delivery_type","additional_allocation","skills","roles"]
  }

@app.route('/addEmployee', methods=['POST'])
@expects_json(schema)
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
    existing_project = session.query(project).filter(project.project_code==data.get("project_code")).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})

    project_list=helper1(existing_project)
    removenull(project_list)
    if project_code in project_list:
        return jsonify({'error':'Employee is already working in the project'})
    project_list.append(project_code)
        
    existing_project.project_code =helper2(project_list)
    session.add(existing_project)
    session.commit()

    try: 
        emp_data = employee(emp_id=data.get("emp_id") , 
                            manager_id = data.get("manager_id"),
                            email = data.get("email") , 
                            first_name = data.get("first_name"), 
                            last_name= data.get("last_name"), 
                            sur_name= data.get("sur_name"), 
                            initial= data.get("initial"), 
                            salutation= data.get("salutation"), 
                            project_code= data.get("project_code"), 
                            dept= data.get("dept"),
                            designation = data.get("designation"),
                            emp_start_date= data.get("emp_start_date",None),
                            emp_last_working_date=data.get("emp_last_date",None),
                            emp_project_assigned_date=data.get("emp_project_assigned_date",None),
                            emp_project_end_date=data.get("emp_project_end",None),

                            employment_status=data.get("employment_status"), 
                            manager_name=data.get("manager_name"), 
                            manager_dept=data.get("manager_dept"), 
                            resource_status=data.get("resource_status"),
                            delivery_type=data.get("delivery_type"),
                            additional_allocation=data.get("additional_allocation"),
                            skills=data.get("skills"),
                            roles=data.get("roles"),

                            )
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
        return jsonify({"error":"Some error happened in adding the employee"}),500


@app.route('/addProjectResource', methods=['POST'])
def addProjectResource():
    session = Session()
    data = request.get_json()
    resource_id = data.get("emp_id")
    project_code = data.get("project_id")
    existing_emp = session.query(employee).filter(employee.emp_id==resource_id).first()
    if existing_emp==None:
        return jsonify({'success':'Employee with ID: {} Does not Exist !'.format(resource_id)})
    
    existing_project = session.query(project).filter(project.project_code==project_code).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})
    print(existing_emp)
    print("<<<<<<<<<<")
    if existing_emp.project_code == None:
        existing_emp.project_code=project_code
        session.add(existing_emp)
        session.commit()
    else:
        existing_proj_code= existing_emp.project_code
        existing_proj_list = helper1(existing_proj_code)
        removenull(existing_proj_list)
        if project_code in existing_proj_list:
            return jsonify({'error':'resource exist already in the project'})
        existing_proj_list.append(project_code)
        
        existing_emp.project_code = helper2(existing_proj_list)# check if the string sanitation is required
        print(type(existing_emp.project_code))
        session.add(existing_emp)
        session.commit()

    # existing_emp.project_code=project_code
    # session.add(existing_emp)
    # session.commit()
    if existing_project.resource_info == None:
        existing_project.resource_info=resource_id
        session.add(existing_project)
        session.commit()
    
    else:
        existing_resource = existing_project.resource_info
        print(existing_resource)
        existing_resource_list=helper1(existing_resource)#helper1 fn convert str to list 
        print(type(existing_resource_list))
        removenull(existing_resource_list)#removed null in list
        print(existing_resource_list)
        if resource_id in existing_resource_list:
            return jsonify({'error':'resource exist already in the project'})
        existing_resource_list.append(resource_id )
        existing_project.resource_info = helper2(existing_resource_list)#helper2 convert list to str 
        print(existing_resource_list)
        session.add(existing_project)
        session.commit()

    session.close()
    return jsonify({"success":"Employee {} and Project {} Linked".format(resource_id,project_code)})

@app.route('/addProjectmanager', methods=['POST'])
def addProjectmanager():
    session = Session()
    data = request.get_json()
    project_code = data.get("project_id")
    project_manager=data.get('manager_id')
    print(project_code)
    print(project_manager)
    existing_project = session.query(project).filter(project.project_code==project_code).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})
    
    existing_project_manager= session.query(employee).filter(employee.manager_id==project_manager).first()
    if existing_project_manager==None:
        return jsonify({"error":"Manager ID {} Does not Exists !".format(project_manager)})

    existing_project_manager.project_code = project_code
    session.add(existing_project_manager)
    session.commit()
    if existing_project.project_manager_id == None:
        existing_project.project_manager_id = project_manager
        session.add(existing_project)
        session.commit()
    else:
        existing_PM = existing_project.project_manager_id
        existing_PM_list = helper1(existing_PM)
        removenull(existing_PM_list)
        if project_manager in existing_PM_list:
            return  jsonify({'error':'Project Manager already Exists in the project'})
        existing_PM_list.append(project_manager)

        existing_project.PM_id=helper2(existing_PM_list)
        print(type(existing_PM_list))
        session.add(existing_project)
        session.commit()
    session.close()
    return jsonify({"success":"Manager {} and Project {} Linked".format(project_manager,project_code)})
        

@app.route('/addProject', methods=['POST'])
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
                                project_start_date=data.get("project_start_date",None),                                
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
    

@app.route("/viewEmpInfo", methods=["POST"])
def viewEmpInfo():
    emp_id = request.json.get("emp_id", None)
    print("????????????")
    print(emp_id)
    if emp_id is None:
        return jsonify({"error":"Employee ID is empty"}), 201
    session = Session()
    emp_objects = session.query(employee).filter(employee.emp_id==emp_id).all()
    print(">>>>>>>>>>>>")
    print(emp_objects)
    if emp_objects == []:
        return jsonify({"error":"Employee Not found !"}), 201
    emp_serialized = serialize_all(emp_objects)
    print(emp_serialized)
    emp_dict = emp_serialized[0]
    project_objects = session.query(project).filter(project.project_code==emp_serialized[0]['project_code']).all()
    if project_objects:
        project_serialized = serialize_all(project_objects)
        proj_dict = project_serialized[0]
        emp_dict.update(proj_dict)
    emp_dict['full_name'] = emp_dict['salutation'] + emp_dict['first_name'] + emp_dict['last_name']
    return jsonify(emp_dict), 201


@app.route("/forgot_pass_create_token", methods=["POST"])
def forgot_pass_create_token():
    session = Session()
    email_id = request.json.get("email_id")
    emp_objects = session.query(employee).filter(employee.email == email_id).first()
    if emp_objects == None:
        return jsonify({"error":" Please enter Valid employee Email Id"})

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
        entities.mail.send_mail("Forgot password setup", Config.MAIL_USERNAME, email_id, html_body, text_body)

        return jsonify(text_body), 201


@app.route("/reset_pass", methods=["POST", "GET"])
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
            return jsonify({'error': 'User not found, This user is not added yet'}), 401
        auth_object.password = password
        session.add(auth_object)
        session.commit()

        return "Password Reset successfully", 200
    else:
        return "Please generate token for reset password  token expired"




if __name__ == '__main__':
    app.run(debug = True)