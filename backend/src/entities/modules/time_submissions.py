from flask import Blueprint, jsonify, request
import datetime
from entities.database import employee,project,authUser,timesubmissions
from entities.database import Session
from entities.database import serialize_all
from entities.modules.auth import jwtvalidate
from entities.helper import date_validation,weeks_in_month,daterange
from sqlalchemy import or_,and_, cast, Date
from sqlalchemy import func 
from calendar import monthrange
from datetime import datetime,timedelta,date
import calendar


time_module = Blueprint(name="time", import_name=__name__)

@time_module.route('/events')
# @jwtvalidate
def events():
    session = Session()
    data= request.get_json()
    user_id=data['user_id']
    current_month=data["month"]
    
    time_objects = session.query(timesubmissions).filter(timesubmissions.user_id==user_id).all()
    serialized_obj = serialize_all(time_objects)
    events_data = []
    for event in serialized_obj:
        eve={}
        eve["title"]="*" + str(event["time_type"]) + " : "+ str(event["hours"]) + " Hours"
        eve["start"]=event["date_info"]
        # eve["start"] = datetime.datetime.strptime(event["date_info"], "%d/%m/%Y").strftime("%d/%m/%Y")
        eve["status"]=event["status"]
        events_data.append(eve)
    return jsonify(events_data),200


@time_module.route('/addtimesubmissions', methods=['POST'])
def addtimesubmissions():    
    data = request.get_json() 
    user_id = data.get('user_id')
    startdate=data.get('startdate')
    enddate=data.get("enddate")
    confirm_sub=data.get("confirm_sub")
    session = Session()
    date_list=list()
    existing_emp = session.query(employee).filter(employee.emp_id == user_id ).first()
    if existing_emp == None:
        return jsonify({'error':'user not available in the employee table'}),400
    if startdate==None and enddate==None:
        return jsonify({"Warning":"Please give Date to add submission"}),400
    if startdate!=None and enddate!=None:
        existing_submission=session.query(timesubmissions.hours).filter(and_(timesubmissions.user_id==data.get('user_id'),cast(timesubmissions.date_info, Date) >= startdate, cast(timesubmissions.date_info, Date) <= enddate)).all()
        hours_list=[emp[0] for emp in existing_submission]
        total_hrs=sum(hours_list)
        s_date=datetime.strptime(startdate, "%Y-%m-%d")
        e_date=datetime.strptime(enddate, "%Y-%m-%d")
        for dt in daterange(s_date, e_date):
            dates=dt.strftime("%Y-%m-%d")
            date_list.append(dates)
        if total_hrs>0:
            if confirm_sub== False:   
                return jsonify({"warning":True}),200
        else:
            for dates in date_list:
                sub_data = timesubmissions( date_info = dates,
                    hours = data.get('hours',None),
                    user_id = data.get('user_id',None).lower(),
                    project_code = data.get('project_id',None),
                    manager_id = data.get('manager_id',None),
                    time_type = data.get('time_type',None).lower(),
                    status = 'unapproved',
                    submission_id = data.get('user_id',None) + data.get('time_type',None) + data.get('hours',None).lower(),
                    task_id=data.get('task_id',None),
                    description=data.get('description',None),
                    remarks=data.get('remarks',None)
                )
                session = Session()
                session.add(sub_data)
                session.commit()
        return jsonify({'success':'Your Time has been  submitted '}),200
    if startdate!=None and enddate==None:
        existing_submission=session.query(timesubmissions.hours).filter(timesubmissions.user_id==data.get('user_id'),timesubmissions.date_info==startdate).all()
        hours_list=[emp[0] for emp in existing_submission]
        total_hrs=sum(hours_list)
        if total_hrs>=8:
            if confirm_sub== False:   
                return jsonify({"warning":True}),200
            else:
                sub_data = timesubmissions( date_info = data.get('startdate',None),
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
            session = Session()
            session.add(sub_data)
            session.commit()
            return jsonify({'success':'Your Time has been  submitted for: {}'.format(data.get('date'))}),200              
        else:
            sub_data = timesubmissions( date_info = data.get('startdate',None),
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
    return (jsonify(serialized_obj)),200


@time_module.route('/getSubmissionsBy', methods=['POST'])
def getSubmissionsBy():
    session = Session()
    data= request.get_json()
    user=data['user_id']
    time_type=data['type']
    if user == 'total' and time_type=='total_unapproved':
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='unapproved').all()
        submit_list=list()
        for sub in sub_objects:
            submits=dict()
            submits["date_info"]= sub.date_info.strftime("%d/%m/%Y")
            submits["description"]= sub.description
            submits["hours"]= sub.hours
            submits["manager_id"]= sub.manager_id
            submits["project_code"]= sub.project_code
            submits["user_id"]= sub.user_id
            submits["time_type"]= sub.time_type
            submits["status"]= sub.status
            submits["remarks"]= sub.remarks
            submits["submission_id"]= sub.submission_id
            submits["task_id"]= sub.task_id
            submit_list.append(submits)
        session.close()
        return (jsonify(submit_list)),200
        
    else:
        sub_objects = session.query(timesubmissions).filter(timesubmissions.status=='unapproved', timesubmissions.user_id==user).all()
        submit_list=list()
        for sub in sub_objects:
            submits=dict()
            submits["date_info"]= sub.date_info.strftime("%d/%m/%Y")
            submits["description"]= sub.description
            submits["hours"]= sub.hours
            submits["manager_id"]= sub.manager_id
            submits["project_code"]= sub.project_code
            submits["user_id"]= sub.user_id
            submits["time_type"]= sub.time_type
            submits["status"]= sub.status
            submits["remarks"]= sub.remarks
            submits["submission_id"]= sub.submission_id
            submits["task_id"]= sub.task_id
            submit_list.append(submits)
        session.close()
        return (jsonify(submit_list)),200


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
        submit_list=list()
        for sub in sub_objects:
            submits=dict()
            submits["id"]=sub.id
            submits["date_info"]= sub.date_info.strftime("%d/%m/%Y"),
            submits["description"]= sub.description
            submits["hours"]= sub.hours
            submits["manager_id"]= sub.manager_id
            submits["project_code"]= sub.project_code
            submits["user_id"]= sub.user_id
            submits["time_type"]= sub.time_type
            submits["status"]= sub.status
            submits["remarks"]= sub.remarks
            submits["submission_id"]= sub.submission_id
            submits["task_id"]= sub.task_id
            submit_list.append(submits)
        session.close()
        return (jsonify(submit_list)),200
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
        submit_list=list()
        for sub in sub_objects:
            submits=dict()
            submits["id"]=sub.id
            submits["date_info"]= sub.date_info.strftime("%d/%m/%Y"),
            submits["description"]= sub.description
            submits["hours"]= sub.hours
            submits["manager_id"]= sub.manager_id
            submits["project_code"]= sub.project_code
            submits["user_id"]= sub.user_id
            submits["time_type"]= sub.time_type
            submits["status"]= sub.status
            submits["remarks"]= sub.remarks
            submits["submission_id"]= sub.submission_id
            submits["task_id"]= sub.task_id
            submit_list.append(submits)
        session.close()
        return (jsonify(submit_list)),200
      

@time_module.route('/timeData', methods=['POST'])
def timeData():
    session = Session()
    data = request.get_json()
    manager_id = data.get("user_id")
    date_submission_obj = session.query(timesubmissions.date_info).all()
    date_info=date_submission_obj
    searchstring = data.get('search')

    from_date = data.get("from_date")
    to_date = data.get("to_date")

    if from_date !=None and to_date!=None:
        query = session.query(timesubmissions.user_id).filter(and_(cast(timesubmissions.date_info, Date) >= from_date, cast(timesubmissions.date_info, Date) <= to_date)).all()
        date_final_list = [q[0].lower() for q in query]
        emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
        emp_final = [emp[0].lower() for emp in emp_list]
        emp_final_list=list(set(date_final_list).intersection(emp_final))
    elif searchstring != None:
        base_query =session.query(timesubmissions.user_id).filter(func.lower(timesubmissions.user_id).contains(searchstring.lower())).distinct(timesubmissions.user_id).all()
        base_final=[emp[0].lower() for emp in base_query]
        emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
        emp_final = [emp[0].lower() for emp in emp_list]
        emp_final_list=list(set(base_final).intersection(emp_final))
    else:
        emp_list = session.query(employee.emp_id).filter(employee.manager_id==manager_id).all()
        emp_final_list = [emp[0].lower() for emp in emp_list]
    time_final = []
    for emp in emp_final_list:
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
        # initial1=initial.upper()
        user_name = (first_name1+" "+last_name)
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
                unapproved = unapproved + time['hours']
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
    # first_name=session.query(employee.first_name).filter(employee.emp_id==emp).first()[0]
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
    session.close()
    return (jsonify({'result':time_final,'total':total_time_list})),200
    

@time_module.route('/review_time', methods=['POST'])
def review_time():
    review_data = request.get_json()
    print(review_data)
    for data in review_data:
        if data['reviewd']==True:
            session = Session()
            username = data['user_id']
            date = datetime.strptime(data['date'], "%d/%m/%Y").date()
            time_type = data['time_type']
            hours = data['hours']
            submission_id=data['submission_id']
            time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours,timesubmissions.submission_id == submission_id).first()
            time_obj.status="approved"
            session.add(time_obj)
            session.commit()
            
        elif data['reviewd']==False:
            session = Session()
            username = data['user_id']
            date =datetime.strptime(data['date'], "%d/%m/%Y").date()
            time_type = data['time_type']
            hours = data['hours']
            time_obj = session.query(timesubmissions).filter(timesubmissions.date_info == date,timesubmissions.user_id == username,timesubmissions.time_type == time_type,timesubmissions.hours == hours).first()
            time_obj.status = "denied"
            session.delete(time_obj)
            session.commit()
            session.close()
    return jsonify({"info":"Time has been reviewed"}),200

@time_module.route('/calendar_data', methods=['POST'])
def calendar_data():
    session = Session()
    data = request.get_json()
    user_id = data.get("user_id")
    current_date=data.get("current_date")
    current_date=datetime.strptime(current_date, '%Y-%m-%d')
    last_day_of_prev_month =current_date.replace(day=1) - timedelta(days=1)
    
    start_day_of_month = current_date.replace(day=1) 
    last_day_of_month=current_date.replace(day = monthrange(current_date.year, current_date.month)[1])
    #user_data
    base_query=session.query(timesubmissions)
    base_query2 = base_query.filter(and_(timesubmissions.user_id==user_id,last_day_of_prev_month <= cast(timesubmissions.date_info, Date) , cast(timesubmissions.date_info, Date) <= last_day_of_month)).all()
    submissions=serialize_all(base_query2)
    
    #Monthly submissions
    events_data = []
    for event in submissions:
        eve={}
        eve["title"]="*" + str(event["time_type"]) + " : "+ str(event["hours"]) + " Hours"
        eve["start"]=event["date_info"]
        # eve["start"] = datetime.datetime.strptime(event["date_info"], "%d/%m/%Y").strftime("%d/%m/%Y")
        eve["status"]=event["status"]
        eve["id"]=event["id"]
        events_data.append(eve)
        print(event["date_info"],"events_data") 
    
    currentMonth = current_date.month
    currentYear = current_date.year

    #Weekly_submissions
    data=[]
    for weekstart, weekend in weeks_in_month(currentYear,currentMonth):
        #weekdata
        base_query2 = session.query(timesubmissions.hours).filter(and_(timesubmissions.user_id==user_id,cast(timesubmissions.date_info, Date) >= weekstart, cast(timesubmissions.date_info, Date) <= weekend)).all()
        hours_list=[hours[0] for hours in base_query2]
        total_hrs=sum(hours_list)
        weekly_submissions=total_hrs
        #week_approved
        base_query3 = session.query(timesubmissions.hours).filter(and_(timesubmissions.user_id==user_id,timesubmissions.status=='approved',cast(timesubmissions.date_info, Date) >= weekstart, cast(timesubmissions.date_info, Date) <= weekend)).all()
        hours_list=[hours[0] for hours in base_query3]
        total_hrs=sum(hours_list)
        approved_submissions=total_hrs
        #week_unapproved
        base_query4 = session.query(timesubmissions.hours).filter(and_(timesubmissions.user_id==user_id,timesubmissions.status=='unapproved',cast(timesubmissions.date_info, Date) >= weekstart, cast(timesubmissions.date_info, Date) <= weekend)).all()
        hours_list=[hours[0] for hours in base_query4]
        total_hrs=sum(hours_list)
        unapproved_submissions=total_hrs
        weekly_data={"weekly_submissions":weekly_submissions,"approved_submissions":approved_submissions,"unapproved_submissions":unapproved_submissions}    
        data.append(weekly_data)
    
    session.close()       
    return(jsonify({'submissions':events_data,"week_data":data})),200
@time_module.route('/delete_submission', methods=['POST'])
def delete():
    data=request.get_json()
    session = Session()
    id_=data.get("id")
    time_obj = session.query(timesubmissions).filter(timesubmissions.id==id_).first()
    session.delete(time_obj)
    session.commit()
    session.close()
    return jsonify({"info": "Submission deleted successfully"}),200