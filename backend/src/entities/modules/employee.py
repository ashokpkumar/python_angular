from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions
from entities.database import Session,department,designation,manager,skill,employeeToSkill
from entities.database import serialize_all
from entities.modules.auth import jwtvalidate
from entities.helper import listToString,stringToList
from sqlalchemy import func
from sqlalchemy import or_,and_ 
from functools import reduce
employee_module = Blueprint(name="employee", import_name=__name__)

@employee_module.route('/employees',methods=["POST"])
def employees():
    session = Session()
    data = request.get_json()
    searchstring = request.args.get('search')
    filter=data.get("filter")
    manager_id=data.get("manager_name",None)
    status=data.get("status",None)
    delivery_type=data.get("delivery_type",None)
    skills = data.get("skills",None)    
    base_query = session.query(employee)
    skill_data=list()
    search_results=0
    if searchstring!= None:
        base_query =base_query.filter(func.lower(employee.emp_id).contains(searchstring.lower())).all()
        serialized_obj = serialize_all(base_query)
        serialed_out = []
    if filter == True:
        query =session.query(employee)       
        if manager_id:
            query = query.filter(employee.manager_id==manager_id) 
        if delivery_type:
            query = query.filter(employee.delivery_type==delivery_type)
        if status:
            query = query.filter(employee.resource_status==status)
        if skills:
            for i in skills:
                query_mapping = session.query(skill.skill_name).filter(skill.id==i).all()
                data_list=[i[0] for i in query_mapping]
                skill_data.append(data_list)
            data=sum(skill_data,[])
            joined_str=",".join(data)
            query = query.filter(employee.skills==joined_str)
        
        filter_query = query.all()
        
        serialized_obj = serialize_all(filter_query)
        serialed_out = []
    else:   
        base_query = session.query(employee).all()
        serialized_obj = serialize_all(base_query)
        serialed_out = []
        
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

@employee_module.route('/addEmployee', methods=['POST'])
def addEmployee():
    data = request.get_json()
    emp_id=data.get("emp_id")
    email=data.get("email")
    project_code=data.get("project_code")
    manager_id=data.get("manager_id")
    roles=data.get("roles")
    skills=data.get("skills")
    session = Session()
    existing_emp = session.query(employee).filter(employee.emp_id==emp_id).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'User ID: {} already exist !'.format(emp_id)})
    existing_emp = session.query(employee).filter(employee.email==email).first()
    if existing_emp:
        session.close()
        return jsonify({'warning':'Email ID: {} already exist !'.format(email)})
    existing_project = session.query(project).filter(project.project_code==project_code).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})
    emp_data = employee(emp_id=data.get("emp_id").lower() , 
                        manager_id = data.get("manager_id"),
                        email = data.get("email").lower(), 
                        first_name = data.get("first_name").lower(), 
                        last_name= data.get("last_name",None), 
                        sur_name= data.get("sur_name",None), 
                        initial= data.get("initial",None), 
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
                        roles=data.get("roles"),

                        )
    if skills!=None:
        skill_list=skills.split(",")
        print("skills",skill_list)
        for i in skill_list:
            exisisting_skill=session.query(skill.id).filter(skill.skill_name==i).all()
            skill_list=[skill[0] for skill in exisisting_skill]
            if exisisting_skill==None:
                return jsonify({"Warning":"skill is not available"})
            skill_data=employeeToSkill(emp_id=data.get("emp_id"),
                                        skill_id=skill_list)
            session.add(skill_data)
        session.commit()
    if roles=='project manager' or roles=='rmg admin':
        manager_data=manager(manager_id=data.get("emp_id"),
                            manager_name=data.get('first_name'),
                            manager_email=data.get("email"),
                            manager_dept=data.get("dept"),
                            project_code= data.get("project_code"),
                            roles=data.get("roles"),
                            reports_to=data.get("manager_id")
                            )
        session = Session()
        session.add(manager_data)
        session.commit() 
        session.close() 
    session = Session()
    session.add(emp_data)
    session.commit()
    
    auth_data = authUser(emp_id = data.get("emp_id").lower(),
                        email=data.get("email").lower(),
                        roles=data.get("roles"))
    session = Session()
    session.add(auth_data)
    print("auth added")
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
    session.close()
    return jsonify(emp_dict), 201

@employee_module.route('/getProjectsInfo',methods=['POST'])
def getProjectsInfo():
    session =Session()
    data =request.get_json()
    emp_id=data.get("emp_id")
    employee_obj = session.query(employee).filter(employee.emp_id==emp_id).first()
    employee_projects_list = employee_obj.project_code.split(",")
    for i in employee_projects_list:
        if i=="":
            employee_projects_list.remove(i)
    projects_info_data = session.query(project).filter(project.project_code.in_(employee_projects_list)).all()
    session.close()
    return jsonify(serialize_all(projects_info_data))


@employee_module.route('/addskills',methods=['POST'])
def addskills():
    data=request.get_json()
    emp_skills=data.get("skill")
    session=Session()
    exisiting_skills=session.query(skill).filter(skill.skill_name==emp_skills).first()
    if exisiting_skills:
        return jsonify({'warning':' {} skill already exist !'.format(emp_skills)}),400
    
    skill_data=skill(skill_name=emp_skills)
    session.add(skill_data)
    session.commit()
    session.close()
    return jsonify({"success":"skill added successfully"}),200    

@employee_module.route('/getskills')
def getskills():
    session = Session()
    skill_objects = session.query(skill).all()
    serialized_obj = serialize_all(skill_objects)
    session.close()
    return (jsonify(serialized_obj))
    
@employee_module.route('/getmanagername')
def getmanagername():
    session = Session()
    base_query = session.query(manager).all()
    # manager_list=[name[0] for name in base_query]
    serialized_obj = serialize_all(base_query)
    return (jsonify(serialized_obj))