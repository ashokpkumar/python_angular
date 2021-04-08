import { Component, CUSTOM_ELEMENTS_SCHEMA, OnInit } from '@angular/core';
import {MatDialogModule} from '@angular/material/dialog';
import {  FormGroup,FormControl } from '@angular/forms';
import {employee} from './employees';
import { addEmployeeService } from './add-employee.service';
@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.css']
})

export class AddEmployeeComponent implements OnInit {
  employee = new employee();
  profileForm = new FormGroup({
    firstName: new FormControl(''),
    lastname: new FormControl(''),
    surname: new FormControl(''),
    initial: new FormControl(''),
    salutation: new FormControl(''),
    managername: new FormControl(''),
    managerdept: new FormControl(''),
    projectid: new FormControl(''),
    empstatus: new FormControl(''),
    dept: new FormControl(''),
    empstartdate: new FormControl(''),
    emplwd: new FormControl(''),
    empprojectassigneddate: new FormControl(''),
    empprojectenddate: new FormControl(''),
    
  });
  public employee_fields_list:any 
  name = new FormControl('');
  constructor(private apiService:addEmployeeService) { }

  ngOnInit(): void {
  
  }
  // addEmployee(){
  //  console.log("name",this.name);
  //  // console.log("adding employee");
    
  // }

  onSubmit() {
    // TODO: Use EventEmitter with form value
    console.log(this.employee);
    this.apiService.addEmployee(this.employee).subscribe(data=>{console.log(data)})
    //console.warn(this.profileForm.value);
  }
}


