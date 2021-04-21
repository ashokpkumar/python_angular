#from .entities.entity import Session, engine, Base

# sources
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
#https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47#:~:text=To%20add%20a%20serialization%20method,columns%20and%20returns%20a%20dictionary.&text=def%20to_dict(self%2C%20show%3D,of%20this%20model.%22%22%22
#sources

from entities.database import employee,project,authUser,timesubmissions,TimeMaster
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
import json
from sqlalchemy.ext.serializer import loads, dumps

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
CORS(app)

Base.metadata.create_all(engine)
#time_master()
create_sample_employee()
@app.route("/setpassword", methods=["POST"])
def setpassword():
    session = Session()
    emp_id = request.json.get("emp_id", None)
    password = request.json.get("password", None)
    auth_object = session.query(authUser).filter(authUser.emp_id == emp_id).first()
    if auth_object is None:
        return jsonify({'error':'User not found, This user is not added yet'}),200
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


@app.route('/projects')
def projects():
    session = Session()
    project_objects = session.query(project).all()
    serialized_obj = serialize_all(project_objects)
    session.close()
    return (jsonify(serialized_obj))


@app.route('/addtimesubmissions', methods=['POST'])
def addtimesubmissions():    
    data = request.get_json()
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
def view_submissions():
    session = Session()
    data = request.get_json()
    manager_name = data   
    existing_submissions = session.query(timesubmissions).filter(timesubmissions.manager_id==manager_name).all()
    if existing_submissions:
        serialized_obj = serialize_all(existing_submissions)
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


@app.route('/timeData', methods=['POST'])
def timeData():
    manager_id = request.get_json()
    session = Session()
    emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
    emp_final = [emp[0].lower() for emp in emp_list]
    time_master_obj = session.query(TimeMaster).all()
    session.close()
    serialized_obj = serialize_all(time_master_obj)
    time_data = []
    for time_info in serialized_obj:
        if time_info["emp_id"].lower() in emp_final:
            time_data.append(time_info)
    time_final = []
    for time in time_data:
        user_id = time["emp_id"]
        user_name = session.query(employee.first_name).filter(employee.emp_id==user_id).first()
        project_time = 0
        sl = 0
        cl = 0
        al = 0
        bench = 0
        month_info =  json.loads(time["timedata"])
        for dates in month_info.keys():
            hour_info_for_date = month_info[dates]
            for time_types in hour_info_for_date:
                if time_types == 'wfh':
                    project_time = project_time + hour_info_for_date[time_types]
                elif time_types == 'CL':
                    cl = cl + hour_info_for_date[time_types]
                elif time_types =='SL':
                    sl = sl +hour_info_for_date[time_types]
                elif time_types =='AL':
                    al = al + hour_info_for_date[time_types]
                elif time_types =='bench':
                    bench = bench + hour_info_for_date[time_types]
        
        time_final.append({'user_id':user_id, 'user_name': user_name[0], 'project_time':project_time,'sl':sl,'cl':cl,'al':al,'bench':bench})
    return (jsonify({'result':time_final}))


@app.route('/review_time', methods=['POST'])
def review_time():
    data = request.get_json()
    print(data)
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


@app.route('/addEmployee', methods=['POST'])
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

    existing_emp.project_code=project_code
    session.add(existing_emp)
    session.commit()
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


if __name__ == '__main__':
    #app.run(host = '0.0.0.0',port = 5000,debug = True)
    app.run(debug = True)