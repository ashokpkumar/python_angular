import { Component, OnInit } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import { projectsApiService } from '../projects/projects.services';
import { addProjectApiService } from './add-projects.service';
import {project} from './projects';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

@Component({
  selector: 'app-add-projects',
  templateUrl: './add-projects.component.html',
  styleUrls: ['./add-projects.component.css']
})

export class AddProjectsComponent implements OnInit {

  project = new project();
  profileForm = new FormGroup({
    clientname: new FormControl(''),
    projectcode: new FormControl(''),
    projectname: new FormControl(''),
    projectstartdate: new FormControl(''),
    projectstatus: new FormControl(''),
    billingtype: new FormControl(''),
    segment: new FormControl(''),
    geography: new FormControl(''),
    solutioncategory: new FormControl(''),
    financialyear: new FormControl(''),
  });
  roles: any
  isVisible: boolean=true;
  constructor(private router: Router,private cookieService: CookieService,private apiService:addProjectApiService,private projectApi: projectsApiService) { }

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
       if ( role=="Admin" || role == "Sales Team") {
         this.isVisible = true;
       } else  {
         this.isVisible = false;
       }
     }
   }

  onSubmit() {

    console.log(this.project)

    this.apiService.addProject(this.project)
    .subscribe(data=>{console.log(data),this.apiService.showMessage(Object.values(data),Object.keys(data))});
    this.router.navigate(["/project"]);
    }
}
