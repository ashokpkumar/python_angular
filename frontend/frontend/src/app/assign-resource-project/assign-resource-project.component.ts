import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {projectResource} from './assign';
import { addProjectResourceApiService } from './assign-resource-project.service';

@Component({
  selector: 'app-assign-resource-project',
  templateUrl: './assign-resource-project.component.html',
  styleUrls: ['./assign-resource-project.component.css']
})
export class AssignResourceProjectComponent implements OnInit {
  roles: any
  isVisible: boolean=true;
  projectResource = new projectResource();
  constructor(private router: Router,private cookieService: CookieService,private apiService:addProjectResourceApiService) { 
  
  }
  
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
       if ( role == "Admin" || role == "RMG Admin") {
         this.isVisible = true;
       } else  {
         this.isVisible = false;
       }
     }
   }
  onSubmit() {
    this.apiService.onSubmit(this.projectResource)
    .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))});
    }
}
