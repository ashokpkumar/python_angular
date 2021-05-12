from flask import Blueprint
from flask import Flask, jsonify, request

from entities.database import employee
from entities.database import Session
from entities.database import serialize_all
from flask_expects_json import expects_json





employees_bp = Blueprint("employees_bp",__name__)


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


@employees_bp.route("/employees")
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




@employees_bp.route('/addEmployee', methods=['POST'])
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



    




@employees_bp.route("/viewEmpInfo", methods=["POST"])
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
