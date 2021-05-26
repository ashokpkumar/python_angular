from entities.database import Session, engine, Base, serialize_all
from entities.database import employee,project,authUser,TimeMaster,timesubmissions
import datetime

emp_list = [
    {'emp_id':'I3228','email':'ashokkumar.p@indiumsoft.com','first_name':'Ashok','last_name':'Kumar','sur_name':'','initial':'P','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Python Lead','emp_start_date':'03/04/2019','emp_last_working_date':'05/06/2020','emp_project_assigned_date':'11/06/2020','emp_project_end_date':'21/07/2020','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'Project Manager ','manager_id':'I3186'},
    {'emp_id':'I31288','email':'amit.kumar@indiumsoft.com','first_name':'Amit','last_name':'Kumar','sur_name':'','initial':'T','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Python Developer','emp_start_date':'20/08/2020','emp_last_working_date':'01/06/2021','emp_project_assigned_date':'05/06/2021','emp_project_end_date':'04/11/2021','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'Employee','manager_id':'I3186'},
    {'emp_id':'I1666','email':'shyam@indiumsoft.com','first_name':'Shyamsundar','last_name':'Mahalingam','sur_name':'','initial':'S','salutation':'Mr','project_code':'DIGI2222','dept':'Digital','designation':'Java Developer','emp_start_date':'11/12/2019','emp_last_working_date':'28/10/2020','emp_project_assigned_date':'20/11/2020','emp_project_end_date':'30/11/2020','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'java','roles':'Sales Team','manager_id':'I3186'},
    {'emp_id':'I1891','email':'RameshThangaraj@indiumsoft.com','first_name':'Ramesh','last_name':'Thangaraj','sur_name':'','initial':'T','salutation':'Mr','project_code':'DIGI2222','dept':'Digital','designation':'Java Developer','emp_start_date':'21/06/2018','emp_last_working_date':'29/11/2019','emp_project_assigned_date':'08/11/2019','emp_project_end_date':'12/11/2019','employment_status':'Project','manager_name':'Ramesh A','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'java','roles':'Delivery Head','manager_id':'I3182'},
    {'emp_id':'I2013','email':'PriyaS@indiumsoft.com','first_name':'Priya','last_name':'S','sur_name':'','initial':'S','salutation':'Ms','project_code':'DIGI2323','dept':'Digital','designation':'SQL developer','emp_start_date':'17/02/2021','emp_last_working_date':'0/11/2020','emp_project_assigned_date':'20/11/2021','emp_project_end_date':'26/12/2021','employment_status':'Project','manager_name':'Karthik Rangamani','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'Project Manager','manager_id':'I3252'},
    {'emp_id':'I3186','email':'nataraj.g@indiumsoft.com','first_name':'Nataraj','last_name':'G','sur_name':'','initial':'G','salutation':'Mr','project_code':'','dept':'Digital','designation':'Project Manager','emp_start_date':'15/10/2020','emp_last_working_date':'0/11/2020','emp_project_assigned_date':'01/10/2020','emp_project_end_date':'03/11/2020','employment_status':'Project','manager_name':'Karthik Rangamani','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'RMG Admin','manager_id':'I3252'},
    {'emp_id':'I3252','email':'r.karthik@indiumsoft.com','first_name':'Karthik','last_name':'Rangamani','sur_name':'','initial':'RK','salutation':'Mr','project_code':'','dept':'Digital','designation':'Vice President','emp_start_date':'10/12/2019','emp_last_working_date':'12/11/2020','emp_project_assigned_date':'21/03/2021','emp_project_end_date':'03/04/2021','employment_status':'Project','manager_name':'Satish Bala','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'','roles':'RMG Admin','manager_id':'I3281'},
    {'emp_id':'I3050','email':'manikandan.l@indiumsoft.com','first_name':'manikandan','last_name':'Loganathan','sur_name':'','initial':'L','salutation':'Mr','project_code':'DIGI1111','dept':'Digital','designation':'Frontend Developer','emp_start_date':'30/10/2020','emp_last_working_date':'04/11/2020','emp_project_assigned_date':'19/09/2021','emp_project_end_date':'21/10/2021','employment_status':'Project','manager_name':'Nataraj.g','manager_dept':'Digital','resource_status':'Billable','delivery_type':'delivery','additional_allocation':'','skills':'react','roles':'Finance Team','manager_id':'I3186'},
    {'emp_id':'I2668','email':'deepak.g@indiumsoft.com','first_name':'Deepak','last_name':'G','sur_name':'','initial':'G','salutation':'Mr','project_code':'DIGI1212','dept':'Digital','designation':'python Developer','emp_start_date':'28/04/2019','emp_last_working_date':'30/11/2020','emp_project_assigned_date':'19/12/2020','emp_project_end_date':'25/01/2021','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'Employee','manager_id':'I3186'},
    {'emp_id':'I3122','email':'chandrasekara.v@indiumsoft.com','first_name':'Chandra ','last_name':'Sekara','sur_name':'','initial':'V','salutation':'Mr','project_code':'DIGI1212','dept':'Digital','designation':'python Developer','emp_start_date':'28/04/2019','emp_last_working_date':'30/11/2020','emp_project_assigned_date':'19/12/2020','emp_project_end_date':'25/01/2021','employment_status':'Project','manager_name':'Nataraj.G','manager_dept':'Digital','resource_status':'billable','delivery_type':'delivery','additional_allocation':'','skills':'python','roles':'Employee','manager_id':'I3186'},
]

project_list = [
    {"clientname":"Indium-Pilit","projectcode":"IND123","projectname":"RMG Web Application ","project_start_date":"14/11/2020","projectstatus":"Submitted","billingtype":"F","segment":"Managed Services","geography":"INDIA","solution_category":"Product Developement","project_manager_id":"I3228,I3186","financialyear":"2021","resource_info":"I31288,I2668,I3050"},
    {"clientname":"AB Martin","projectcode":"ABMPPSW_FCUD20","projectname":"Port from Powershell to Web Application","project_start_date":"04/01/2021","projectstatus":"In Progress","billingtype":"F","segment":"Consulting Services","geography":"US","solution_category":"Data Analytics","project_manager_id":"I3186","financialyear":"2019","resource_info":'I31288,I2668'},
    {"clientname":"GNQ-IND","projectcode":"AWLD_TMIN12","projectname":"RMG Application for Management","project_start_date":"01/02/2019","projectstatus":"Submitted","billingtype":"T","segment":"Managed Services","geography":"INDIA","solution_category":"Product Developement","project_manager_id":"I3228,I3186","financialyear":"2020","resource_info":"I3122,I2668"},
    {"clientname":"Pi-Lit","projectcode":"AQTFDHW_TMIN18","projectname":"RMG Application for Management ","project_start_date":"22/08/2020","projectstatus":"Submitted-pending request ","billingtype":"F","segment":"Consulting Services","geography":"INDIA","solution_category":"Product Developement","project_manager_id":"I3186","financialyear":"2019","resource_info":"I3228,I31288,I3050"},
    {"clientname":"ACT Fibernet","projectcode":"BKMPPSW_F202","projectname":"Hadoop Data Platform Consulting","project_start_date":"12/06/2019","projectstatus":"Not Approved","billingtype":"T","segment":"Managed Services","geography":"US","solution_category":"Analytics","project_manager_id":"I2013","financialyear":"2019","resource_info":"I3050,I1666"},
    {"clientname":"Adqvest","projectcode":"MPPSWB_FCUD203","projectname":"Financial data Harvesting from web sources","project_start_date":"09/12/2019","projectstatus":"In Progress","billingtype":"T","segment":"Consulting Services","geography":"US","solution_category":"Product Developement","project_manager_id":"I3228","financialyear":"2021","resource_info":"I3122,I31288"},
    {"clientname":"Bharath","projectcode":"BMKPPSW_FCUD204","projectname":"Client Insurance Source and Services ","project_start_date":"01/07/2019","projectstatus":"Submitted-pending request","billingtype":"F","segment":"Consulting Services","geography":"INDIA","solution_category":"Big Data Analytics","project_manager_id":"I3186","financialyear":"2021","resource_info":"I3228,I2013"},
    {"clientname":"AppTech","projectcode":"SWRRP_FUD205","projectname":"ARDAMS Powershell Web Application","project_start_date":"10/03/2021","projectstatus":"In Progress","billingtype":"F","segment":"Consulting Services","geography":"US","solution_category":"Product Developement","project_manager_id":"I3252","financialyear":"2019","resource_info":"I3186,I3228"},
    {"clientname":"ABB Technology","projectcode":"PPSWFF_FCUD206","projectname":"Production Based Data Platform","project_start_date":"18/05/2020","projectstatus":"Approval Rejected","billingtype":"F","segment":"Consulting Services","geography":"INDIA","solution_category":"Big Data Analytics","project_manager_id":"I3252","financialyear":"2020","resource_info":"I1891,I1666,I3050"},
    {"clientname":"VNN Softcore","projectcode":"QWWST_HPPR24","projectname":"Data Corelation from Web Application","project_start_date":"28/11/2020","projectstatus":"In Progress","billingtype":"F","segment":"Consulting Services","geography":"INDIA","solution_category":"Product Developement","project_manager_id":"I3281,I3252","financialyear":"2018","resource_info":"I3252,I3186"},
    {"clientname":"INB services","projectcode":"PQQE_XGGL21","projectname":"Resource Management for INB","project_start_date":"02/03/2021","projectstatus":"In Progress","billingtype":"T","segment":"Consulting Services","geography":"US","solution_category":"Product Developement","project_manager_id":"I3228","financialyear":"2021","resource_info":"I2668,I3122"},
    {"clientname":"Airbnb","projectcode":"WGLOR_LMNV03","projectname":"Frimware Developement","project_start_date":"09/03/2019","projectstatus":"Pending Request","billingtype":"F","segment":"Managed Services","geography":"INDIA","solution_category":"Big Data Analytics","project_manager_id":"I2013","financialyear":"2020","resource_info":"I3050,I1666"},

]

timesubmission_list =[

    #Askok(changed order of time type and status to show with permutation data in table because it only stores data with uniqe user Id )
    {"date":"12/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Submitted-pending approval","submission_id":"i3228i3228wfh"},
    {"date":"16/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Approved","submission_id":"i3228i3228wfh"},
    {"date":"20/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Unapproved","submission_id":"i3228i3228wfh"},

    {"date":"13/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Submitted-pending approval","submission_id":"i3228i3228SL"},
    {"date":"15/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Approved","submission_id":"i3228i3228SL"},
    {"date":"19/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Unapproved","submission_id":"i3228i3228SL"},

    {"date":"11/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Submitted-pending approval","submission_id":"i3228i3228CL"},
    {"date":"23/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Approved","submission_id":"i3228i3228CL"},
    {"date":"25/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Unapproved","submission_id":"i3228i3228CL"},
    
    {"date":"22/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Submitted-pending approval","submission_id":"i3228i3228AL"},
    {"date":"27/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Approved","submission_id":"i3228i3228AL"},
    {"date":"29/01/2021","hours":"8","user_id":"I3228","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Unapproved","submission_id":"i3228i3228AL"},
    #Amit
    {"date":"16/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Approved","submission_id":"I31288I31288wfh"},
    {"date":"12/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I31288I31288wfh"},
    {"date":"20/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Unapproved","submission_id":"I31288I31288wfh"},

    {"date":"8/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Submitted-pending approval","submission_id":"I31288I31288SL"},
    {"date":"14/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Approved","submission_id":"I31288I31288SL"},
    {"date":"21/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Unapproved","submission_id":"I31288I31288SL"},

    {"date":"24/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Submitted-pending approval","submission_id":"I31288I31288CL"},
    {"date":"26/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Approved","submission_id":"I31288I31288CL"},
    {"date":"29/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Unapproved","submission_id":"I31288I31288CL"},

    {"date":"29/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Submitted-pending approval","submission_id":"I31288I31288AL"},
    {"date":"02/02/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Approved","submission_id":"I31288I31288AL"},
    {"date":"09/01/2021","hours":"8","user_id":"I31288","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Unapproved","submission_id":"I31288I31288AL"},
    #Deepak
    {"date":"29/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Unapproved","submission_id":"I2668I2668SL"},
    {"date":"02/02/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Submitted-pending approval","submission_id":"I2668I2668SL"},
    {"date":"06/02/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Approved","submission_id":"I2668I2668SL"},

    {"date":"12/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I2668I2668wfh"},
    {"date":"16/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Approved","submission_id":"I2668I2668wfh"},
    {"date":"20/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Unapproved","submission_id":"I2668I2668wfh"},

    {"date":"14/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Submitted-pending approval","submission_id":"I2668I2668CL"},
    {"date":"21/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Approved","submission_id":"I2668I2668CL"},
    {"date":"27/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Unapproved","submission_id":"I2668I2668CL"},

    {"date":"29/01/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Submitted-pending approval","submission_id":"I2668I2668AL"},
    {"date":"02/02/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Approved","submission_id":"I2668I2668AL"},
    {"date":"09/02/2021","hours":"8","user_id":"I2668","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Unapproved","submission_id":"I2668I2668AL"},
    #RameshThangaraj
    {"date":"18/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"Cl","status":"Submitted-pending approval","submission_id":"I1891I1891CL"},
    {"date":"20/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"CL","status":"Approved","submission_id":"I1891I1891CL"},
    {"date":"27/02/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"CL","status":"Unapproved","submission_id":"I1891I1891CL"},

    {"date":"19/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I1891I1891wfh"},
    {"date":"28/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"wfh","status":"Approved","submission_id":"I1891I1891wfh"},
    {"date":"04/04/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"wfh","status":"Unapproved","submission_id":"I1891I1891wfh"},

    {"date":"10/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"SL","status":"Submitted-pending approval","submission_id":"I1891I1891SL"},
    {"date":"26/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"SL","status":"Approved","submission_id":"I1891I1891SL"},
    {"date":"03/04/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"Sl","status":"Unapproved","submission_id":"I1891I1891SL"},

    {"date":"29/02/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"AL","status":"Submitted-pending approval","submission_id":"I1891I1891AL"},
    {"date":"02/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"Al","status":"Approved","submission_id":"I1891I1891AL"},
    {"date":"09/03/2021","hours":"8","user_id":"I1891","project_id":"DIG156","manager_id":"I3182","time_type":"AL","status":"Unapproved","submission_id":"I1891I1891AL"},
    #Priya
    {"date":"29/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"AL","status":"Submitted-pending approval","submission_id":"I2013I2013AL"},
    {"date":"02/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"AL","status":"Approved","submission_id":"I2013I2013AL"},
    {"date":"09/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"AL","status":"Unapproved","submission_id":"I2013I2013AL"},

    {"date":"18/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I2013I2013wfh"},
    {"date":"26/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"wfh","status":"Approved","submission_id":"I2013I2013wfh"},
    {"date":"10/03/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"wfh","status":"Unapproved","submission_id":"I2013I2013wfh"},

    {"date":"22/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"SL","status":"Submitted-pending approval","submission_id":"I2013I2013SL"},
    {"date":"19/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"SL","status":"Approved","submission_id":"I2013I2013SL"},
    {"date":"01/03/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"SL","status":"Unapproved","submission_id":"I2013I2013SL"},

    {"date":"06/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"CL","status":"Submitted-pending approval","submission_id":"I2013I2013CL"},
    {"date":"17/02/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"CL","status":"Approved","submission_id":"I2013I2013CL"},
    {"date":"05/03/2021","hours":"8","user_id":"I2013","project_id":"DIG132","manager_id":"I3252","time_type":"CL","status":"Unapproved","submission_id":"I2013I2013CL"},
    #Mani kandan
    {"date":"12/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Unapproved","submission_id":"I3050I3050wfh"},
    {"date":"16/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I3050I3050wfh"},
    {"date":"20/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"wfh","status":"Approved","submission_id":"I3050I3050wfh"},

    {"date":"28/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Submitted-pending approval","submission_id":"I3050I3050wfh"},
    {"date":"15/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Approved","submission_id":"I3050I3050wfh"},
    {"date":"22/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"SL","status":"Unapproved","submission_id":"I3050I3050wfh"},

    {"date":"04/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Submitted-pending approval","submission_id":"I3050I3050wfh"},
    {"date":"19/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Approved","submission_id":"I3050I3050wfh"},
    {"date":"11/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"CL","status":"Unapproved","submission_id":"I3050I3050wfh"},

    {"date":"29/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Submitted-pending approval","submission_id":"I3050I3050wfh"},
    {"date":"02/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Approved","submission_id":"I3050I3050wfh"},
    {"date":"09/02/2021","hours":"8","user_id":"I3050","project_id":"DIG123","manager_id":"I3186","time_type":"AL","status":"Unapproved","submission_id":"I3050I3050wfh"},
    #R.karthic
    {"date":"08/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"CL","status":"Submitted-pending approval","submission_id":"I3252I3252CL"},
    {"date":"10/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"CL","status":"Approved","submission_id":"I3252I3252CL"},
    {"date":"17/02/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"CL","status":"Unapproved","submission_id":"I3252I3252CL"},

    {"date":"01/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"wfh","status":"Submitted-pending approval","submission_id":"I3252I3252wfh"},
    {"date":"14/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"wfh","status":"Approved","submission_id":"I3252I3252wfh"},
    {"date":"26/02/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"wfh","status":"Unapproved","submission_id":"I3252I3252wfh"},

    {"date":"02/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"SL","status":"Submitted-pending approval","submission_id":"I3252I3252SL"},
    {"date":"19/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"SL","status":"Approved","submission_id":"I3252I3252SL"},
    {"date":"27/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"SL","status":"Unapproved","submission_id":"I3252I3252SL"},

    {"date":"04/03/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"AL","status":"Submitted-pending approval","submission_id":"I3252I3252AL"},
    {"date":"29/02/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"AL","status":"Approved","submission_id":"I3252I3252AL"},
    {"date":"18/02/2021","hours":"8","user_id":"I3252","project_id":"DIG129","manager_id":"I3281","time_type":"AL","status":"Unapproved","submission_id":"I3252I3252AL"},


    #{"date":"08/02/2021","hours":"8","user_id":"Shekar","project_id":"DIG123","manager_id":"Natraj","time_type":"wfh","status":"Submitted-pending approval","submission_id":"ShekarShekarwfh"},
    #{"date":"06/02/2021","hours":"8","user_id":"Manikandan","project_id":"TE146","manager_id":"Prabhu","time_type":"wfh","status":"Submitted-pending approval","submission_id":"ManikandanManikandanwfh"},
    #{"date":"12/02/2021","hours":"8","user_id":"Subramani","project_id":"TE026","manager_id":"Thakur","time_type":"wfh","status":"Submitted-pending approval","submission_id":"SubramaniSubramaniwfh"},
    #{"date":"20/02/2021","hours":"8","user_id":"Raghu","project_id":"DIG101","manager_id":"Siva","time_type":"wfh","status":"Submitted-pending approval","submission_id":"RaghuRaghuwfh"},
    #{"date":"09/03/2021","hours":"8","user_id":"Sam","project_id":"DIG291","manager_id":"Vinoth","time_type":"wfh","status":"Submitted-pending approval","submission_id":"SamSamwfh"},
    #{"date":"24/03/2021","hours":"8","user_id":"Nithesh","project_id":"TE013","manager_id":"Shanmugam","time_type":"wfh","status":"Submitted-pending approval","submission_id":"NitheshNitheshwfh"},
    #{"date":"30/03/2021","hours":"8","user_id":"Ram","project_id":"DIG1234","manager_id":"Ravi","time_type":"wfh","status":"Submitted-pending approval","submission_id":"RamRamwfh"},
    #{"date":"13/04/2021","hours":"8","user_id":"Aravind","project_id":"DIG135","manager_id":"Dinesh","time_type":"wfh","status":"Submitted-pending approval","submission_id":"AravindAravindwfh"},
    #{"date":"19/04/2021","hours":"8","user_id":"Vineet","project_id":"TE074","manager_id":"Prashanth","time_type":"wfh","status":"Submitted-pending approval","submission_id":"VineetVineetwfh"}

]

authUser_list=[
    {"emp_id":"Manager","email":"manager@gamil.com","password":"manager@123","roles":"Manager"},
    {"emp_id":"Lead","email":"lead@gmail.com","password":"lead@123","roles":"Lead"},
    {"emp_id":"Sales_lead","email":"sales@gmail.com","password":"sales@123","roles":"Sales_lead"},
    {"emp_id":"VP","email":"Vp@gmail.com","password":"vp@123","roles":"VP"},
    {"emp_id":"Admin","email":"admin@gamail.com","password":"admin@123","roles":"Admin"},
    {"emp_id":"Employee","email":"employee@gmail.com","password":"employee@123","roles":"Employee"},
    
    {"emp_id":"I3228","email":"ashokkumar.p@gmail.com","password":"ashokkumar@123","roles":"Employee,Project Manager"},
    {"emp_id":"I31288","email":"amit.kumar@gmail.com","password":"amit@123","roles":"Employee"},
    {"emp_id":"I1666","email":"shyam@gmail.com","password":"shyam@123","roles":"Employee,Sales Team"},
    {"emp_id":"I1891","email":"RameshThangaraj@gmail.com","password":"RameshThangaraj@123","roles":"Employee,Delivery Head"},
    {"emp_id":"I2013","email":"PriyaS@gmail.com","password":"Priya@123","roles":"Employee,Project Manager"},
    {"emp_id":"I3186","email":"nataraj.g@gmail.com","password":"employee@123","roles":"Employee,RMG Admin"},
    {"emp_id":"I3252","email":"r.karthik@gmail.com","password":"karthik@123","roles":"Employee,RMG Admin"},
    {"emp_id":"I3050","email":"manikandan.l@gmail.com","password":"manikandan@123","roles":"Employee,Finance Team"},
    {"emp_id":"I2668","email":"deepak.g@gmail.com","password":"deepak@123","roles":"Employee"},
    {"emp_id":"I3122","email":"chandrasekara.v@gmail.com","password":"chandrasekara@123","roles":"Employee"},

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
    for sample in project_list:
        session = Session()
        sample_objects = session.query(project).filter(project.project_code==sample["projectcode"]).first()
        #serialized_obj = serialize_all(emp_objects)
        if sample_objects==None:
            sample_data = project(client_name = sample["clientname"],
                                    project_code=sample["projectcode"],
                                    project_name=sample["projectname"],
                                    project_start_date=sample["project_start_date"],
                                    project_status=sample["projectstatus"],
                                    billing_type=sample["billingtype"],
                                    segment=sample["segment"],
                                    geography=sample["geography"],
                                    solution_category =sample["solution_category"],
                                    financial_year = sample["financialyear"],
                                    resource_info = sample["resource_info"]
                                )         
            print(sample_data)  
            session.add(sample_data)
            session.commit()
        session.close()


def create_sample_timesubmissions():    
    for timesubmission in timesubmission_list: 
        session = Session()
        sub_objects = session.query(timesubmissions).filter(timesubmissions.date_info==timesubmission["date"]).first()
        if sub_objects==None:
            sub_data = timesubmissions( date_info=timesubmission['date'],
                                            hours = timesubmission['hours'],
                                            user_id = timesubmission['user_id'],
                                            project_code = timesubmission['project_id'],
                                            manager_id = timesubmission['manager_id'],
                                            time_type = timesubmission['time_type'],
                                            status = timesubmission["status"],
                                            submission_id = timesubmission["submission_id"]    
                                    )
            print(sub_data)
            session.add(sub_data)
            session.commit()    
        session.close()

def create_sample_authUser():    
    for authUsers in authUser_list:
        session = Session()
        auth_objects = session.query(authUser).filter(authUser.emp_id==authUsers["emp_id"]).first()
        if auth_objects==None: 
            auth_data = authUser( emp_id =authUsers["emp_id"], 
                                    email = authUsers["email"],
                                    password = authUsers["password"],
                                    roles = authUsers["roles"]
                                    )
            print(auth_data)
            session.add(auth_data)
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