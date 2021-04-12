from entities.database import Session, engine, Base, serialize_all
from entities.database import employee,project,authUser,TimeMaster
import datetime

def create_sample_employee(): 
    session = Session()
    emp_objects = session.query(employee).first()
    #serialized_obj = serialize_all(emp_objects)
    if not emp_objects:
        emp_data = employee(emp_id = "i3128",
                            first_name="ashok" , 
                            last_name = "kumar", 
                            sur_name= "", 
                            initial= "P", 
                            salutation= "Mr", 
                            project_code= "DIGI12345", 
                            dept= "DIGITAL", 

                            emp_start_date= datetime.datetime.now(),
                            emp_last_working_date=datetime.datetime.now(),
                            emp_project_assigned_date=datetime.datetime.now(),
                            emp_project_end_date=datetime.datetime.now(),

                            employment_status="INPROJECT", 
                            manager_name="NATARAJ", 
                            manager_dept="DIGITAL", 
                            resource_status = "BILLABLE",
                            delivery_type = "MANAGED SERVICES",
                            additional_allocation = "",
                            skills = "APP developement",
                            roles = "ADMIN"
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
