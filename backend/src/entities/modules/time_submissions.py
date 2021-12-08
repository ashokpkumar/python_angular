from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions
from entities.database import Session
from entities.database import serialize_all
from entities.modules.auth import jwtvalidate


time_module = Blueprint(name="time", import_name=__name__)

@time_module.route('/events')
def events():
    session = Session()
    time_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(time_objects)
    events_data = []
    for event in serialized_obj:
        eve={}
        eve["title"]="*" + str(event["time_type"]) + " : "+ str(event["hours"]) + " Hours"
        eve["start"]=event["date_info"]
        eve["start"] = datetime.datetime.strptime(event["date_info"], "%d/%m/%Y").strftime("%m-%d-%Y")
        eve["status"]=event["status"]
        events_data.append(eve)   
    return jsonify(events_data)


@time_module.route('/addtimesubmissions', methods=['POST'])
def addtimesubmissions():    
    data = request.get_json() 
    user_id = data.get('user_id')
    session = Session()
    existing_emp = session.query(employee).filter(employee.emp_id == user_id ).first()
    if existing_emp == None:
        return jsonify({'error':'user not available in the employee table'}),200
    # if existing_emp:
    #     existing_type=session.query(timesubmissions.date_info==data.get('date')).filter(timesubmissions.time_type==data.get('time_type'),timesubmissions.hours!=data.get('hours')).first()
    #     return({'error':'Hours is already filled'})
    else:
        sub_data = timesubmissions( date_info = data.get('date',None),
                                        hours = data.get('hours',None),
                                        user_id = data.get('user_id',None).lower(),
                                        project_code = data.get('project_id',None),
                                        manager_id = data.get('manager_id',None),
                                        time_type = data.get('time_type',None).lower(),
                                        status = 'unapproved',
                                        submission_id = data.get('user_id',None) + data.get('user_id',None) + data.get('time_type',None).lower(),
                                        task_id=data.get('task_id',None),
                                        description=data.get('description',None),
                                        remarks=data.get('remarks',None)     
                                    )
    # existing_type=session.query(timesubmissions.date_info==data.get('date')).filter(timesubmissions.time_type==data.get('time_type')).all
    # if existing_type:
    #     return jsonify({'error':"same time type"})
    session = Session()
    session.add(sub_data)
    session.commit()
    return jsonify({'success':'Your Time has been  submitted for: {}'.format(data.get('date'))}),200


@time_module.route('/view_submissions', methods=['POST'])
def viewsubmissions():
    session = Session()
    data = request.get_json()
    manager_name = data  
    emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_name).all()
    emp_final = [emp[0].lower() for emp in emp_list]
    submission_obj = session.query(timesubmissions).filter(timesubmissions.manager_id.in_(emp_final),timesubmissions.status=='Unapproved' ).all()
    if submission_obj:
        serialized_obj = serialize_all(submission_obj)
        return jsonify(serialized_obj),200
    return jsonify({'info':'Time Submissions available for you'}),200
  

@time_module.route('/timesubmissions')
# @jwtvalidate
def timesubmission():
    session = Session()
    sub_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(sub_objects)
    session.close()
    return (jsonify(serialized_obj))


@time_module.route('/getSubmissionsBy', methods=['POST'])
def getSubmissionsBy():
    session = Session()
    user = request.get_json()
    if user == 'total':
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='unapproved').all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200
        
    else:
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='unapproved', timesubmissions.user_id==user).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200


@time_module.route('/getTimeBy', methods=['POST'])
def getTimeBy():
    session = Session()
    data = request.get_json()
    time_type = data['type']
    user = data['user']

    if user == 'total':
        if time_type =="project":
            time_type_list = ['wfh','REG','project']
        elif time_type=="total_hrs":
                time_type_list=['wfh','project','REG','cl','sl','al','bench','non_project']
         
        elif time_type=="total_presence":
                time_type_list=['wfh','project','REG','bench','non_project']
        
        elif time_type=="total_absence":
                time_type_list=['cl','sl','al']
        else:
            time_type_list = [time_type]
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='approved',timesubmissions.time_type.in_(time_type_list)).all()
        serialized_obj = serialize_all(sub_objects)

        session.close()
        return (jsonify(serialized_obj)),200
    else:
        if time_type =="project":
            time_type_list = ['wfh','REG','project']
        elif time_type=="total":
                time_type_list=['wfh','project','REG','cl','sl','al','bench','non_project']
         
        elif time_type=="total_presence":
                time_type_list=['wfh','project','REG','bench','non_project']
        
        elif time_type=="total_absence":
                time_type_list=['cl','sl','al']
          
        else:
            time_type_list = [time_type]
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='approved',timesubmissions.time_type.in_(time_type_list),timesubmissions.user_id==user).all()
        serialized_obj = serialize_all(sub_objects)
        session.close()
        return (jsonify(serialized_obj)),200
      

@time_module.route('/timeData', methods=['POST'])
# @jwtvalidate
def timeData():
    session = Session()
    data = request.get_json()
    manager_id = data.get("user_id")
    date_submission_obj = session.query(timesubmissions.date_info).all()
    date_info=date_submission_obj
    # min_date=min(date_info)
    # max_date=max(date_info)
    
    emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
    emp_final = [emp[0].lower() for emp in emp_list]
    time_final = []
    for emp in emp_final:
        project_time = 0
        sl = 0
        cl=0
        al=0
        non_project=0
        bench=0
        user_id = emp
        unapproved=0
        first_name=session.query(employee.first_name).filter(employee.emp_id==emp).first()[0]
        last_name=session.query(employee.last_name).filter(employee.emp_id==emp).first()[0]                
        initial=session.query(employee.initial).filter(employee.emp_id==emp).first()[0]
        first_name1=first_name.capitalize()
        initial1=initial.upper()
        user_name = (first_name1+" "+last_name +"."+ initial1)
        submission_obj = session.query(timesubmissions).filter(timesubmissions.user_id==emp).all()#timesubmissions.date_info == datee,
        serialized_obj = serialize_all(submission_obj)
        for time in serialized_obj:
            if time['status']=='approved':
                if time['time_type']=='wfh' or time['time_type']=='project':
                    project_time = project_time + time['hours']
                elif time['time_type']=='sl':
                    sl = sl + time['hours']
                elif time['time_type']=='cl':
                    cl = cl + time['hours']
                elif time['time_type']=='al':
                    al = al + time['hours']
                elif time['time_type']=='non_project':
                    non_project = non_project + time['hours']
                elif time['time_type']=='bench':
                    bench = bench + time['hours']
            else:
                unapproved =time['hours']
        print(unapproved)
        total_hrs = project_time + sl + cl + al + bench + non_project
        total_presence = project_time + non_project + bench 
        total_absence = sl + cl + al 
        time_final.append({'user_id':user_id, 'user_name': user_name, 'project_time':project_time,'sl':sl,'cl':cl,'al':al,'non_project':non_project,'bench':bench,'unapproved':unapproved,'total_presence': total_presence,'total_absence':total_absence,'total_hrs':total_hrs})
    total_project = 0
    total_sl = 0
    total_cl = 0
    total_al = 0
    total_total_presence=0
    total_total_absence=0
    total_non_project=0
    total_bench = 0
    total_total_hrs=0
    total_unapproved = 0
    first_name=session.query(employee.first_name).filter(employee.emp_id==emp).first()[0]
    for emp_data in time_final:
        total_project = total_project  + emp_data['project_time']
        total_sl = total_sl  + emp_data['sl']   
        total_cl = total_cl  + emp_data['cl']
        total_total_presence = total_total_presence  + emp_data['total_presence']
        total_total_absence = total_total_absence  + emp_data['total_absence']
        total_total_hrs = total_total_hrs  + emp_data['total_hrs']
        total_al = total_al  + emp_data['al']
        total_non_project=total_non_project + emp_data['non_project']
        total_bench = total_bench  + emp_data['bench']
        total_unapproved = total_unapproved + emp_data['unapproved']
    total_time_list = {'total_project':total_project,'total_total_presence':total_total_presence,'total_total_absence':total_total_absence,'total_sl':total_sl,'total_cl':total_cl,'total_al':total_al,'total_non_project':total_non_project,'total_bench':total_bench,'total_total_hrs':total_total_hrs,'total_unapproved':total_unapproved, }
    
    return (jsonify({'result':time_final,'total':total_time_list}))
    

@time_module.route('/review_time', methods=['POST'])
def review_time():
    data = request.get_json()
    if data['reviewd']==True:
        session = Session()
        username = data['user_name']
        date = data['date']
        time_type = data['time_type']
        hours = data['hours']
        datee = datetime.datetime.strptime(date, "%d/%m/%Y")
        month = datee.month
        year = datee.year
        time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours).first()
        time_obj.status = "approved"
        session.add(time_obj)
        session.commit()
        session.close()
        return jsonify({"info":"Time has been reviewed"})

    elif data['reviewd']==False:
        session = Session()
        username = data['user_name']
        date = data['date']
        time_type = data['time_type']
        hours = data['hours']
        datee = datetime.datetime.strptime(date,  "%d/%m/%Y")
        month = datee.month
        year = datee.year
        time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours).first()
        time_obj.status = "denied"
        session.add(time_obj)
        session.commit()
        session.close()
        return jsonify({"info":"Time has been reviewed"})

