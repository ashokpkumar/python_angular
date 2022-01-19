from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions,department,designation
from entities.database import Session
from entities.database import serialize_all
from entities.modules.auth import jwtvalidate
from entities.helper import listToString,stringToList
from sqlalchemy import func 
employee_module = Blueprint(name="employee", import_name=__name__)

@employee_module.route('/employees')
def employees():
    session = Session()
    data = request.get_json()
    searchstring = request.args.get('search')
    print(searchstring)
    base_query = session.query(employee)
    search_results=0
    if searchstring!= None:
        base_query =base_query.filter(func.lower(employee.emp_id).contains(searchstring.lower())).all()
        serialized_obj = serialize_all(base_query)
        serialed_out = []
    else:
        emp_objects = session.query(employee).all()
        serialized_obj = serialize_all(emp_objects)
        serialed_out = []
    print("seriali",serialized_obj)
    for dictionary in serialized_obj:
        dictionary['full_name'] = dictionary['first_name'] + dictionary['last_name']
        dictionary['project_code'] = stringToList(dictionary['project_code'])
        serialed_out.append(dictionary)
    project_objects = session.query(project).all()
    serialized_project = serialize_all(project_objects)
    for dictionary in serialed_out:
        emp_id = dictionary["project_code"]
        for proj_item in serialized_project:
            if proj_item["project_code"]==emp_id:
                proj_item["project_code"] = [emp_id] #Project id should return list instead of string in employee
                dictionary.update(proj_item)
                print(dictionary)
                break
    session.close()
    return (jsonify(serialed_out))

@employee_module.route('/getmanagerdata')#get unique mangerid data from employee table 
def managerdata():
    session = Session()
    emp_objects = session.query(employee).all()
    serialized_obj1 = serialize_all(emp_objects)
    managerid=[]#list to store unique managerid
    userdata=[]#list to store first user which have unique managers
    for i in serialized_obj1:
        data=i['manager_id']
        managerid.append(data)
    data=list(set(managerid))
    for i in data:    
        emp_objects1 = session.query(employee.emp_id).filter(employee.manager_id==i).first()#get userids for managerslist
        for i in emp_objects1:
            emp_objects = session.query(employee).filter(employee.emp_id==i).all()
            serialized_obj=serialize_all(emp_objects)
            userdata.append(serialized_obj)
    print("d",userdata)
    session.close()
    # print(serialized_obj)
    return (jsonify(serialized_obj1))



@employee_module.route('/getprojectid')
def getproject():
    # project_id=[]
    session = Session()
    project_objects = session.query(project).all()
    serialized_obj = serialize_all(project_objects)
    print(serialized_obj)
    session.close()
    return (jsonify(serialized_obj))
    # session = Session()
    # emp_projectid = session.query(project.project_code).all()
    # print(emp_projectid)
    # projectid_list=emp_projectid
    # print(projectid_list)
    # print('>>>>>>')
    # session.close()
    # return (jsonify(projectid_list))
@employee_module.route('/getdepartment')
def getdepartment():
    session = Session()
    department_objects = session.query(department).all()
    serialized_obj = serialize_all(department_objects)
    session.close()
    return (jsonify(serialized_obj))
@employee_module.route('/getdesignation')
def getdesignation():
    session = Session()
    designation_objects = session.query(designation).all()
    serialized_obj = serialize_all(designation_objects)
    session.close()
    return (jsonify(serialized_obj))

@employee_module.route('/addDepartment', methods=['POST'])
def addDepartment():    
    data = request.get_json()
    department_name=data.get("department_name")
    print(type(department_name))
    session = Session()
    existing_dept = session.query(department).filter(department.department_name==data.get("department_name")).first()
    if existing_dept:
        session.close()
        return jsonify({'warning':'{} Department is already exist !'.format(data.get("department_name"))})
    dept_data=department(department_name=data.get("department_name")
                         )
    session = Session()
    session.add(dept_data)
    session.commit()
    session.close()
    return jsonify({"success":"{} Department is created successfully".format(department_name)}), 201

@employee_module.route('/addDesignation', methods=['POST'])
def addDesignation():    
    data = request.get_json()
    desig= data.get('designation')
    print(type(desig))
    session = Session()
    existing_designation = session.query(designation).filter(designation.designation==desig).first()
    if existing_designation:
        session.close()
        return jsonify({'warning':'{} designation is already exist !'.format(desig)})
    designation_data=designation(designation =data.get("designation").lower())
    print(type(designation_data))
    session = Session()
    session.add(designation_data)
    session.commit()
    session.close()
    return jsonify({"success":"{} Designation is created successfully".format(desig)}), 201



# @employee_module.route('/managercheck', methods=['POST'])
# def managerCheck():
#     data=request.get_json()
#     manager_id=data.get("manager_id")
#     print(data.get("manager_id"))
#     # manager_name=data.get('manager_name')
#     session=Session()
#     existing_manager=session.query(employee).filter(employee.manager_id==manager_id).first()
#     if existing_manager == None:
#         session.close()
#         return jsonify({'warning':'Manager ID does not exist !'})
#     # existing_manager_name =session.query(employee.manager_name).filter(employee.manager_id==manager_id)).first()
#     return jsonify(manager_id)
    
@employee_module.route('/addEmployee', methods=['POST'])
def addEmployee():
    data = request.get_json()
    emp_id=data.get("emp_id")
    email=data.get("email")
    project_code=data.get("project_code")
    manager_id=data.get("manager_id")
    session = Session()
    existing_emp = session.query(employee).filter(employee.emp_id==emp_id).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'User ID: {} already exist !'.format(emp_id)})
    #print(emp_id)
    existing_emp = session.query(employee).filter(employee.email==email).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'Email ID: {} already exist !'.format(email)})
    existing_project = session.query(project).filter(project.project_code==project_code).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})
    
    # existing_manager=session.query(employee).filter(employee.manager_id==manager_id).first()
    # if existing_manager == None:
    #     session.close()
    #     return jsonify({'warning':'Manager ID does not exist !'})

    emp_data = employee(emp_id=data.get("emp_id").lower() , 
                        manager_id = data.get("manager_id"),
                        email = data.get("email").lower(), 
                        first_name = data.get("first_name").lower(), 
                        last_name= data.get("last_name").lower(), 
                        sur_name= data.get("sur_name").lower(), 
                        initial= data.get("initial").lower(), 
                        salutation= data.get("salutation").lower(), 
                        project_code= data.get("project_code").lower(), 
                        dept= data.get("dept").lower(),
                        designation = data.get("designation").lower(),
                        emp_start_date= data.get("emp_start_date",None),
                        emp_last_working_date=data.get("emp_last_date",None),
                        emp_project_assigned_date=data.get("emp_project_assigned_date",None),
                        emp_project_end_date=data.get("emp_project_end",None),

                        employment_status=data.get("employment_status").lower(), 
                        manager_name=data.get("manager_name").lower(), 
                        manager_dept=data.get("manager_dept").lower(), 
                        resource_status=data.get("resource_status").lower(),
                        delivery_type=data.get("delivery_type").lower(),
                        additional_allocation=data.get("additional_allocation").lower(),
                        skills=data.get("skills").lower(),
                        roles=listToString(data.get("roles")),

                        )
    session = Session()
    session.add(emp_data)
    session.commit()
    auth_data = authUser(emp_id = data.get("emp_id").lower(),
                        email=data.get("email").lower(),
                        roles=listToString(data.get("roles")))
    session = Session()
    session.add(auth_data)
    session.commit()     
    return jsonify({"success":"successfully added employee {}".format(data.get("emp_id"))}),200     
    # except:
    #     return jsonify({"error":"Some error happened in adding the employee"}),500

@employee_module.route("/viewEmpInfo", methods=["POST"])
def viewEmpInfo():
    emp_id = request.json.get("emp_id", None)
    # print("????????????")
    # print(emp_id)
    if emp_id is None:
        return jsonify({"error":"Employee ID is empty"}), 201
    session = Session()
    # print(emp_id)
    emp_objects = session.query(employee).filter(employee.emp_id==emp_id).all()
    # print(">>>>>>>>>>>>")
    # print(emp_objects)
    if emp_objects == []:
        return jsonify({"error":"Employee Not found !"}), 201
    emp_serialized = serialize_all(emp_objects)
    # print(emp_serialized)
    emp_dict = emp_serialized[0]
    project_objects = session.query(project).filter(project.project_code==emp_serialized[0]['project_code']).all()
    if project_objects:
        project_serialized = serialize_all(project_objects)
        proj_dict = project_serialized[0]
        emp_dict.update(proj_dict)
    
    first_name=session.query(employee.first_name).filter(employee.emp_id==emp_id).first()[0]
    last_name=session.query(employee.last_name).filter(employee.emp_id==emp_id).first()[0]                
    initial=session.query(employee.initial).filter(employee.emp_id==emp_id  ).first()[0]
    first_name1=first_name.capitalize()
    initial1=initial.upper()
    user_name = (first_name1+" "+last_name +"."+ initial1)
    emp_dict['full_name'] = user_name
    return jsonify(emp_dict), 201


