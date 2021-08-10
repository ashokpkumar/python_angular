import { Component, OnInit } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import { projectsApiService } from '../projects/projects.services';
import { addProjectApiService } from './add-projects.service';
import {project,users} from './projects';
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
  public users:any
  roles: any
  isVisible: boolean=false;
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
  
     for (const role of userRoles) {
      if ( role==users.admin,users.rmgadmin,users.sales_team) {
        this.isVisible = true;
       } 
     }
   }

  onSubmit() {

    

    this.apiService.addProject(this.project)
    .subscribe(data=>{
      this.apiService.showMessage(Object.values(data),Object.keys(data))});
    this.router.navigate(["/project"]);
    }
}
