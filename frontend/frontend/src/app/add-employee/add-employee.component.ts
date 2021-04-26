import { Component, CUSTOM_ELEMENTS_SCHEMA, OnInit,ViewEncapsulation } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import {employee} from './employees';
import { addEmployeeService } from './add-employee.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {MatCalendarCellClassFunction,MatDatepickerModule} from '@angular/material/datepicker';

//https://www.itsolutionstuff.com/post/how-to-use-toaster-notification-in-angular-8example.html
@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.css'],
  encapsulation: ViewEncapsulation.None,
})


export class AddEmployeeComponent implements OnInit {
  durationInSeconds = 5;
  employee = new employee();
  // profileForm = new FormGroup({
  //   firstName: new FormControl(''),
  //   lastname: new FormControl(''),
  //   surname: new FormControl(''),
  //   initial: new FormControl(''),
  //   salutation: new FormControl(''),
  //   managername: new FormControl(''),
  //   managerdept: new FormControl(''),
  //   projectid: new FormControl(''),
  //   empstatus: new FormControl(''),
  //   dept: new FormControl(''),
  //   empstartdate: new FormControl(''),
  //   emplwd: new FormControl(''),
  //   empprojectassigneddate: new FormControl(''),
  //   empprojectenddate: new FormControl(''),
    
  // });
  public employee_fields_list:any 
  name = new FormControl('');
  constructor(private apiService:addEmployeeService,private router: Router,private cookieService: CookieService) { }
  public roles="";
  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){
    this.roles=this.cookieService.get('roles');
    }
    else{
      this.router.navigate(['/login']);
    }
  }
 
  onSubmit() {
    
    console.log(this.employee);
    this.apiService.addEmployee(this.employee).subscribe(data=>{this.apiService.showMessage(Object.values(data),Object.keys(data))})
   
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