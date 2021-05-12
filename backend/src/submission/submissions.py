from flask import Blueprint
from flask import Flask, jsonify, request

from entities.database import employee, timesubmissions
from entities.database import Session
from entities.database import serialize_all


submission_bp = Blueprint("submission_bp",__name__)




@submission_bp.route('/addtimesubmissions', methods=['POST'])
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


@submission_bp.route('/view_submissions', methods=['POST'])
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
  

@submission_bp.route('/timesubmissions')
def timesubmission():
    session = Session()
    sub_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(sub_objects)
    session.close()
    return (jsonify(serialized_obj))

@submission_bp.route('/getSubmissionsBy', methods=['POST'])
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