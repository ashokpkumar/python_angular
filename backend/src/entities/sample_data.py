from entities.database import Session, engine, Base, serialize_all
from entities.database import employee,project,authUser,TimeMaster
import datetime

emp_list = [
    {'emp_id':'i3228','email':'ashokkumar.p@indiumsoft.com','first_name':'Ashok','last_name':'Kumar','sur_name':'','initial':'P','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Python Lead','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'admin','manager_id':'I3186'},
    {'emp_id':'i31288','email':'amit.kumar@indiumsoft.com','first_name':'Amit','last_name':'Kumar','sur_name':'','initial':'T','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Python Developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'admin','manager_id':'I3186'},
    {'emp_id':'I1666','email':'shyam@indiumsoft.com','first_name':'Shyamsundar','last_name':'Mahalingam','sur_name':'','initial':'S','salutation':'Mr','project_code':'DIGI2222','dept':'Digital','designation':'Java Developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'java','roles':'','manager_id':'I3186'},
    {'emp_id':'I1891','email':'RameshThangaraj@indiumsoft.com','first_name':'Ramesh','last_name':'Thangaraj','sur_name':'','initial':'T','salutation':'Mr','project_code':'DIGI2222','dept':'Digital','designation':'Java Developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Ramesh A','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'java','roles':'','manager_id':'i3182'},
    {'emp_id':'I2013','email':'PriyaS@indiumsoft.com','first_name':'Priya','last_name':'S','sur_name':'','initial':'S','salutation':'Ms','project_code':'DIGI2323','dept':'Digital','designation':'SQL developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Karthik Rangamani','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'','manager_id':'I3252'},
    {'emp_id':'I3186','email':'nataraj.g@indiumsoft.com','first_name':'Nataraj','last_name':'G','sur_name':'','initial':'G','salutation':'Mr','project_code':'','dept':'Digital','designation':'Project Manager','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Karthik Rangamani','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'admin,manager','manager_id':'I3252'},
    {'emp_id':'I3252','email':'r.karthik@indiumsoft.com','first_name':'Karthik','last_name':'Rangamani','sur_name':'','initial':'RK','salutation':'Mr','project_code':'','dept':'Digital','designation':'Vice President','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Satish Pala','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'admin,manager','manager_id':''},
    {'emp_id':'I3050','email':'manikandan.l@indiumsoft.com','first_name':'manikandan','last_name':'Loganathan','sur_name':'','initial':'L','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Frontend Developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Nataraj.g','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'react','roles':'admin','manager_id':'I3186'},
    {'emp_id':'I2668','email':'deepak.g@indiumsoft.com','first_name':'Deepak','last_name':'G','sur_name':'','initial':'G','salutation':'Mr','project_code':'DIGI1212','dept':'Digital','designation':'python Developer','emp_start_date':'','emp_last_working_date':'','emp_project_assigned_date':'','emp_project_end_date':'','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'admin','manager_id':'I3186'}
]

def create_sample_employee(): 
    for emp in emp_list:
        session = Session()
        emp_object = session.query(employee).filter(employee.emp_id==emp['emp_id']).first()
        if emp_object==None:
            emp_data = employee(emp_id = emp['emp_id'],
                            manager_id = emp['manager_id'],
                            email = emp['email'],
                            first_name = emp['first_name'],
                            last_name = emp['last_name'],
                            sur_name = emp['sur_name'],
                            initial = emp['initial'],
                            salutation = emp['salutation'],
                            project_code = emp['project_code'],
                            dept = emp['dept'],
                            designation = emp['designation'],
                            emp_start_date = emp['emp_start_date'],
                            emp_last_working_date = emp['emp_last_working_date'],
                            emp_project_assigned_date = emp['emp_project_assigned_date'],
                            emp_project_end_date = emp['emp_project_end_date'],
                            employment_status = emp['employment_status'],
                            manager_name = emp['manager_name'],
                            manager_dept = emp['manager_dept'],
                            resource_status = emp['resource_status'],
                            delivery_type = emp['delivery_type'],
                            skills = emp['skills'],
                            roles = emp['roles']

                            )
            session.add(emp_data)
            session.commit()
        session.close()


def create_sample_project(): 
    session = Session()
    project_objects = session.query(project).first()
    #serialized_obj = serialize_all(emp_objects)
    if not project_objects:
        project_objects = project(client_name = "Pi-Lit",
                            project_code="DIGI12345" , 
                            project_name = "Pi-lit", 
                            project_start_date=  datetime.datetime.now(),
                            project_status= "In Progress", 
                            billing_type= "F", 
                            segment= "Consulting Services", 
                            geography= "US", 
                            solution_category="Product Development", 
                            financial_year="2020", 
                            
                            )
        session.add(project_objects)
        session.commit()
        session.close()


def time_master():
    session = Session()
    time_objects = session.query(TimeMaster).first()
    if not time_objects:
        time_objects = TimeMaster(emp_id="i3128",
                                  month="01",
                                  year="2021",
                                  timedata=""
                                  )
        session.add(time_objects)
        session.commit()
        session.close()
