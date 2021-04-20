//https://ng-bootstrap.github.io/#/components/modal/examples

import { Component, OnInit } from '@angular/core';
import {Subscription} from 'rxjs';
import { projectsApiService } from './projects.services';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {projectResource} from './assign';
import {FormControl} from '@angular/forms';
import {MatSelectModule} from '@angular/material/select';
@Component({
  selector: 'app-view-projects',
  templateUrl: './view-projects.component.html',
  styleUrls: ['./view-projects.component.css']
})
export class ViewProjectsComponent implements OnInit {
  projectResource = new projectResource();

  public project_list: any;
  public employee_list: any;

  projectListSubs: Subscription;

  closeResult = '';
  public sample_data:string;
  
  constructor(private modalService: NgbModal,private router: Router,private projectApi: projectsApiService,private cookieService: CookieService) { }

  ngOnInit(): void {

    if (this.cookieService.get('login')=='true'){
      this.projectListSubs = this.projectApi
      .getProjects()
      .subscribe(res=>{this.project_list=res;
    
      },
    
      ) ;
      this.projectListSubs = this.projectApi
      .getEmployees()
      .subscribe(res=>{this.employee_list=res;
        console.log("Employee List: ",res)
      },
 
      ) ;


    }else{
   
      this.router.navigate(['/login']);
    }
    
  }
  addResource(projectResource){
 
  this.projectApi.addProjectResource(this.projectResource)
  .subscribe(data=>{
  
    this.projectApi.showMessage(Object.values(data),Object.keys(data))});
  this.projectListSubs = this.projectApi
      .getProjects()
      .subscribe(res=>{this.project_list=res;
     
      },

        );
      this.router.navigate(['/project']);
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate(['/project']);
  }


  open(content,project_code) {
    this.projectResource.project_id = project_code;
  
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
 
       console.log("Project resource",this.projectResource);
      this.addResource(this.projectResource);
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
   
    });
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
}
