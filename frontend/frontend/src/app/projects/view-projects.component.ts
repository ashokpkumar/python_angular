import { Component, OnInit } from '@angular/core';
import {Subscription} from 'rxjs';
import { projectsApiService } from './projects.services';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-view-projects',
  templateUrl: './view-projects.component.html',
  styleUrls: ['./view-projects.component.css']
})
export class ViewProjectsComponent implements OnInit {
  public project_list: any;
  projectListSubs: Subscription;
  public projectResource:string;
  constructor(private router: Router,private projectApi: projectsApiService,private cookieService: CookieService) { }

  ngOnInit(): void {
    console.log("TOKEN from ngoninit",this.cookieService.get("access_token"));
    console.log("Username",this.cookieService.get('username'));
    console.log("roles",this.cookieService.get('roles'));
    console.log('login',this.cookieService.get('login'));
    if (this.cookieService.get('login')=='true'){
      this.projectListSubs = this.projectApi
      .getProjects()
      .subscribe(res=>{this.project_list=res;console.log(res)},console.error) ;
    }else{
      console.log("Redirect");
      this.router.navigate(['/login']);
    }
    
  }
  addResource(projectResource){
  console.log(projectResource);
  }

}
