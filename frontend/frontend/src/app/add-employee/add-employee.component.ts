import { Component, CUSTOM_ELEMENTS_SCHEMA, OnInit,ViewEncapsulation } from '@angular/core';
import {  FormGroup,FormControl, Validators } from '@angular/forms';
import {employee,users,project} from './employees';
import { addEmployeeService } from './add-employee.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {MatCalendarCellClassFunction,MatDatepickerModule} from '@angular/material/datepicker';
import { subscribeOn } from 'rxjs/operators';

//https://www.itsolutionstuff.com/post/how-to-use-toaster-notification-in-angular-8example.html
@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.css'],
  encapsulation: ViewEncapsulation.None,
})


export class AddEmployeeComponent implements OnInit {
  [x: string]: any;
  durationInSeconds = 5;
  employee = new employee();
  emailPattern =  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  isValidFormSubmitted: boolean = false;
  public users:any
  roles: any
  isVisible: boolean=false;
  project= new project();
  manager_id:any
  manager_name:any
  public proj_list:any;
  public dept_List: any
  public desig_List: any
  project_code:any
  department_name:any
  designation:any

  // employee = new FormGroup({
  //   emp_id : new FormControl(),
  //   email : new FormControl(),
  //   firstName:new FormControl(),
  //   lastname:new FormControl(),
  //   surname:new FormControl(),
  //   initial:new FormControl(),
  //   salutation:new FormControl(),
  //   managername:new FormControl(),
  //   project_code:new FormControl(),
  //   geography:new FormControl(),
  //   dept:new FormControl(),
  //   designation:new FormControl(),
  //   emp_start_date:new FormControl(),
  //   emp_last_working_date:new FormControl(),
  //   emp_project_assigned_date:new FormControl(),
  //   emp_project_end_date:new FormControl(),
  //   employment_status:new FormControl(),
  //   manager_name:new FormControl(),
  //   manager_dept:new FormControl(),
  //   resource_status:new FormControl(),
  //   delivery_type:new FormControl(),
  //   additional_allocation:new FormControl(),
  //   skills:new FormControl(),
  //   roles:new FormControl()

  // });
  public employee_fields_list:any
  name = new FormControl('');
  constructor(private apiService:addEmployeeService,private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (window.sessionStorage.getItem('login')=='true'){
    this.roles=window.sessionStorage.getItem('roles');
     this.checkRoles(this.roles);
    }
    else{
      this.router.navigate(['/login']);
    }
    this.apiService.getprojectid()
    .subscribe(res=>{
      console.log(res) 
      this.proj_list = res,
      console.log(res)                 
        });
    this.apiService.getdepartment().subscribe(res=>{
      console.log(res)
      this.dept_list=res
    });
    this.apiService.getdesignation().subscribe(res=>{
      console.log(res)
      this.desig_list=res
    });
  }
  checkRoles(roles) {
   let userRoles = roles.split(",");
   console.log(userRoles);
    for (const role of userRoles) {
      if ( role==users.admin,users.rmgadmin) {
        this.isVisible = true;
      } 
    }
  }
  // projectid(){
  //   this.apiService.getprojectid()
  //   .subscribe(res=>{
  //     console.log(res) 
  //     this.project_code = res,
  //     console.log(res)                 
  //       });
  // }
  // checkManger(manager_id){
  //   this.manager_id=this.employee.manager_id
  //   console.log(this.employee.manager_id)
  //   this.apiService.checkmanager(this.manager_id)
  //   .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))})
  // }

  

  onSubmit(data) {
    console.log(this.employee)
    this.isValidFormSubmitted = false;

    if (data.email.invalid) {
       return;
    }

    this.isValidFormSubmitted = true;
    console.log(this.employee)
    this.apiService.addEmployee(this.employee)
    .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))})
    console.log(this.employee)

    

    // this.router.navigate(["/employee"]);
  }


  // dateClass: MatCalendarCellClassFunction<Date> = (cellDate, view) => {
  //   // Only highligh dates inside the month view.
  //   if (view === 'month') {
  //     const date = cellDate.getDate();

  //     // Highlight the 1st and 20th day of each month.
  //     return (date === 1 || date === 20) ? 'example-custom-date-class' : '';
  //   }

  //   return '';
  // }
}
