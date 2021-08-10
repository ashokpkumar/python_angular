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
  projectResource = new projectResource();
  constructor(private router: Router,private cookieService: CookieService,private apiService:addProjectResourceApiService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
  }
  onSubmit() {
    this.apiService.onSubmit(this.projectResource)
    .subscribe(data=>{
      this.apiService.showMessage(Object.values(data),Object.keys(data))});
    }
}
