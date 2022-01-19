
from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions
from entities.database import Session
from entities.database import serialize_all
from entities.helper import stringToList,listToString
project_module = Blueprint(name="projects", import_name=__name__)

@project_module.route('/projects')
def projects():
    session = Session()
    project_objects = session.query(project).all()
    serialized_obj = serialize_all(project_objects)
    session.close()
    return (jsonify(serialized_obj))

@project_module.route('/addProjectResource', methods=['POST'])
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
    print("<<<<<<<<<<")
    resource_data=existing_emp.emp_id
    print(resource_data)
    if existing_emp.project_code == None:
        existing_emp.project_code=project_code
        session.add(existing_emp)
        session.commit()
    else:
        existing_proj_code= existing_emp.project_code
        existing_proj_list = stringToList(existing_proj_code)
        if project_code in existing_proj_list:
            return jsonify({'error':'resource exist already in the project'})
        existing_proj_list.append(project_code)
        
        existing_emp.project_code = listToString(existing_proj_list)# check if the string sanitation is required
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
        existing_resource_list=stringToList(existing_resource)#stringToList fn convert str to list 
        print(type(existing_resource_list))
        print(existing_resource_list)
        if resource_id in existing_resource_list:
            return jsonify({'error':'resource exist already in the project'})
        existing_resource_list.append(resource_id )
        existing_project.resource_info = listToString(existing_resource_list)#listToString convert list to str 
        print(existing_resource_list)
        session.add(existing_project)
        session.commit()

    session.close()
    return jsonify({"success":"Employee {} and Project {} Linked".format(resource_id,project_code)})

@project_module.route('/removeProjectResource',methods=['POST'])
def removeresource():
    session=Session()
    data=request.get_json()
    emp_id=data.get("emp_id")
    project_code=data.get("project_id")
    print("<<<<<<<<<<<<")
    print(emp_id)
    print("<<<<<<<<<<<<")
    print(project_code)
    project_=session.query(project).filter(project.project_code==project_code).first()
    project_resources_list=project_.resource_info.split(",")
    print("<<<<<<<<<<<<")
    print(project_resources_list)
    try:
        project_resources_list.remove(emp_id)
    except:
        pass
    print(project_resources_list)
    out_PM =''
    for i in project_resources_list:
        out_PM = i + "," + out_PM

    project_.resource_info = out_PM
    session.add(project_)
    session.commit()
    session.close()

    emp_=session.query(employee).filter(employee.emp_id==emp_id).first()
    emp_project_list=emp_.project_code.split(",")
    print("<<<<<<<<<<<<<<")
    print(emp_project_list)
    try:
        emp_project_list.remove(project_code)
    except:
        pass
    print(emp_project_list)
    out_proj=""
    for i in emp_project_list:
        out_proj= i+","+out_proj
    
    emp_.project_code=out_proj
    session.add(emp_)
    session.commit()   
    session.close()

    return jsonify({"success":"Resource {} removed from project".format(emp_id)})

@project_module.route('/getResourceInfo',methods=['POST'])
def getResourceInfo():
    session =Session()
    data =request.get_json()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    project_ = session.query(project).filter(project.project_code==data).first()
  
    project_resources_list = project_.resource_info.split(",")
    for i in project_resources_list:
        if i=="":
            project_resources_list.remove(i)
    resource_info_data = session.query(employee).filter(employee.emp_id.in_(project_resources_list)).all()
    print(serialize_all(resource_info_data))
    session.close()
    return jsonify(serialize_all(resource_info_data))
  
@project_module.route('/addProjectmanager', methods=['POST'])
def addProjectmanager():
    session = Session()
    data = request.get_json()
    project_code = data.get("project_id")
    project_manager=data.get('manager_id')

    existing_project = session.query(project).filter(project.project_code==project_code).first()
    if existing_project==None:
        return jsonify({'error':'Project with ID: {} Does not Exist !'.format(project_code)})
    
    existing_project_manager= session.query(employee).filter(employee.manager_id==project_manager).first()
    if existing_project_manager==None:
        return jsonify({"error":"Manager ID {} Does not Exists !".format(project_manager)})

    if existing_project.project_manager_id == None:
        existing_project.project_manager_id = project_manager
        session.add(existing_project)
        session.commit()
    else:
        existing_PM = existing_project.project_manager_id
  
        existing_PM_list = stringToList(existing_PM)

        if project_manager in existing_PM_list:
            return  jsonify({'error':'Project Manager already Exists in the project'})
        existing_PM_list.append(project_manager)
   
        existing_project.project_manager_id=listToString(existing_PM_list)

        session.add(existing_project)
        session.commit()
    session.close()
    return jsonify({"success":"Manager {} and Project {} Linked".format(project_manager,project_code)})
        
@project_module.route('/addProject', methods=['POST'])
def addProject():
    data = request.get_json()
    project_code=data.get("projectcode")
    session = Session()
    existing_project = session.query(project).filter(project.project_code==project_code).first()
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

    # try:     
    #     project_data = project(client_name = data.get("clientname").lower(),
    #                             project_code=data.get("projectcode").lower(),
    #                             project_name=data.get("projectname").lower(),
    #                             project_start_date=data.get("project_start_date",None),                                
    #                             project_status=data.get("projectstatus").lower(),
    #                             billing_type=data.get("billingtype").lower(),
    #                             segment=data.get("segment").lower(),
    #                             geography=data.get("geography").lower(),
    #                             solution_category =data.get("solutioncategory").lower(),
    #                             financial_year = data.get("financialyear").lower()
        
    #     )
    #     session = Session()
    #     session.add(project_data)
    #     session.commit()
    #     session.close()
    #     return jsonify({"success":"added data to the table successfully"}), 201
    # except:
    #     return jsonify({"error":"Something happened while adding the data to the table, please check the data and try again"}), 500
    