import { Component, OnInit } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import { addDesignationService } from './add-designation.service';
import { designation, users } from './designation-info';

@Component({
  selector: 'app-add-designation',
  templateUrl: './add-designation.component.html',
  styleUrls: ['./add-designation.component.css']
})


export class AddDesignationComponent implements OnInit {
  designation = new designation();
  public users:any
  roles: any
  isVisible: boolean=false;
constructor(private router: Router,private cookieService: CookieService,private apiService:addDesignationService) { }

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
  console.log(this.designation)
  this.apiService.addDesignation(this.designation)
  .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))})
  console.log(this.designation)
}
}