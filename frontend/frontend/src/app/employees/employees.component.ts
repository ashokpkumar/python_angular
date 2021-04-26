import { Component, OnInit } from '@angular/core';
import {Subscription} from 'rxjs';
import {employeesApiService} from './employees.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {projectResource} from './assign';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  public employee_list: any;
  public project_list: any;
  empListSubs: Subscription;
  projectListSubs: Subscription;
  projectResource = new projectResource();
  
  constructor(private modalService: NgbModal,private empApi: employeesApiService,private router: Router,private cookieService: CookieService) { }
  public roles="";
  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){
    this.roles=this.cookieService.get('roles');
    }
    else{
      this.router.navigate(['/login']);
    }
    this.empListSubs = this.empApi
                            .getExams()
                            .subscribe(res=>{this.employee_list=res;

                              console.log(this.employee_list);
                            },console.error) ;
                            this.projectListSubs = this.empApi
      .getProjects()
      .subscribe(res=>{this.project_list=res;
         console.log(res)
      },

      ) ;
  }
  addResource(projectResource){
    console.log(projectResource.emp_id);
    console.log(projectResource.project_id);
    this.empApi.addProjectResource(this.projectResource)
  .subscribe(data=>{

    this.empApi.showMessage(Object.values(data),Object.keys(data))});
    this.router.navigate(['/employee']);
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['/employee']);
  }
  open(content,project_code) {
    this.projectResource.emp_id = project_code;
     console.log('Project Code: ',project_code);
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {

      this.addResource(this.projectResource);
    }, (reason) => {

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
