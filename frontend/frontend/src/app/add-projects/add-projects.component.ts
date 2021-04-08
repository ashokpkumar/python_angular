import { Component, OnInit } from '@angular/core';
import {  FormGroup,FormControl } from '@angular/forms';
import { projectsApiService } from '../projects/projects.services';
import { addProjectApiService } from './add-projects.service';
import {project} from './projects';
@Component({
  selector: 'app-add-projects',
  templateUrl: './add-projects.component.html',
  styleUrls: ['./add-projects.component.css']
})

export class AddProjectsComponent implements OnInit {
  //public project_list: any;
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
  constructor(private apiService:addProjectApiService,private projectApi: projectsApiService) { }

  ngOnInit(): void {
  }
  onSubmit() {
    // TODO: Use EventEmitter with form value

    console.log(this.project)
    
    this.apiService.addProject(this.project)
    .subscribe(data=>{console.log(data)})
   // console.warn(this.profileForm.value);
    //this.projectApi.getProjects().subscribe(res=>{this.project_list=res;console.log(res)},console.error) ;
  }
}
