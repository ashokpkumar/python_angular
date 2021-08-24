import { Component, OnInit } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import { addDepartmentService } from './add-department.service';
import { department, users } from './department-info';

@Component({
  selector: 'app-add-department',
  templateUrl: './add-department.component.html',
  styleUrls: ['./add-department.component.css']
})


export class AddDepartmentComponent implements OnInit {
  department = new department();
  public users:any
  roles: any
  isVisible: boolean=false;
constructor(private router: Router,private cookieService: CookieService,private apiService:addDepartmentService) { }

ngOnInit(): void {
  if (this.cookieService.get('login')=='true'){
  this.roles=this.cookieService.get('roles');
  this.checkRoles(this.roles)
  }
  else{
    this.router.navigate(['/login']);
  }
}
checkRoles(roles) {
  let userRoles = roles.split(",");
  console.log(userRoles);
   for (const role of userRoles) {
    if ( role==users.rmgadmin) {
      this.isVisible = true;
     } 
   }
 }
 onSubmit(data) {
  console.log(this.department)
  this.apiService.addDepartment(this.department)
  .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))})
  console.log(this.department)
}
}