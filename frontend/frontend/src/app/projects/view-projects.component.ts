//https://ng-bootstrap.github.io/#/components/modal/examples

import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { projectsApiService } from './projects.services';
import { CookieService } from 'ngx-cookie-service';
import { Router } from "@angular/router"
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { projectResource,users } from './assign';
import { projectManager } from './assignPM';
import { FormControl } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { faSearch, faSlidersH, faTimesCircle } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-view-projects',
  templateUrl: './view-projects.component.html',
  styleUrls: ['./view-projects.component.css']
})
export class ViewProjectsComponent implements OnInit {
  projectResource = new projectResource();
  projectManager = new projectManager();

  public project_list: any;
  public employee_list: any;
  public copyProjList: any
  public copyEmpList: any

  project_name: any
  project_id: any
  client_name: any
  public users:any
  roles: any
  isVisible: boolean=false;

  projectListSubs: Subscription;
  searchInput:String;
  closeResult = '';
  public sample_data: string;
  faSearch = faSearch
  faTimesCircle = faTimesCircle
  faSlidersH = faSlidersH
  dataForFilter = {
    selectedProject: "All",
    projectID: "All",
    clientName: "All",
  }
  constructor(private modalService: NgbModal, private router: Router, private projectApi: projectsApiService, private cookieService: CookieService) { }

  ngOnInit(): void {

    if (this.cookieService.get('login') == 'true') {
     this.roles=this.cookieService.get('roles');
     this.checkRoles(this.roles);


      this.projectListSubs = this.projectApi
        .getProjects()
        .subscribe(res => {
          this.project_list = res;
          console.log("project_list",this.project_list)
          this.copyProjList = res
          let project_name = []
          let project_id = []
          let client_name = []
          this.project_list.map(item=>{
            if(item['project_name']!=""){
              project_name.push(item['project_name'])
            }
            if(item['project_code']!=""){
              project_id.push(item['project_code'])
            }
            if(item['client_name']!=""){
              client_name.push(item['client_name'])
            }
          })
          this.project_name= new Set(project_name)
          this.project_id= new Set(project_id)
          this.client_name = new Set(client_name)
        },

        );
      this.projectListSubs = this.projectApi
        .getEmployees()
        .subscribe(res => {
          this.employee_list = res;
        },

        );


    } else {

      this.router.navigate(['/login']);
    }

  }
    addmanager(projectManager){

     this.projectApi.addProjectManager(this.projectManager)
       .subscribe(data => {

         this.projectApi.showMessage(Object.values(data), Object.keys(data))
       });
     this.projectListSubs = this.projectApi
       .getEmployees()
       .subscribe(res => {
         this.employee_list = res;
         this.copyEmpList = res
       },

       );
     this.router.navigate(['/project']);
     this.router.routeReuseStrategy.shouldReuseRoute = () => false;
     this.router.onSameUrlNavigation = 'reload';
     this.router.navigate(['/project']);
    }
   open1(contentPM,project_code ) {
     this.projectManager.project_id = project_code;

     this.modalService.open(contentPM, { ariaLabelledBy: 'modal-basic-title' }).result.then((result) => {
       this.closeResult = `Closed with: ${result}`;

       console.log("Project Manager", this.projectManager);
       this.addmanager(this.projectManager);
     }, (reason) => {
       this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;

     });
   }

   checkRoles(roles) {
   let userRoles = roles.split(",");
   console.log(userRoles);
    for (const role of userRoles) {
      if ( role==users.admin) {
        this.isVisible = true;
      } 
    }
  }

  addResource(projectResource) {

    this.projectApi.addProjectResource(this.projectResource)
      .subscribe(data => {

        this.projectApi.showMessage(Object.values(data), Object.keys(data))
      });
    this.projectListSubs = this.projectApi
      .getProjects()
      .subscribe(res => {
        this.project_list = res;
        this.copyProjList = res
      },

      );
    this.router.navigate(['/project']);
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['/project']);

    }

  open(content, project_code) {
    this.projectResource.project_id = project_code;

    this.modalService.open(content, { ariaLabelledBy: 'modal-basic-title' }).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;

      console.log("Project resource", this.projectResource);
      this.addResource(this.projectResource);
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;

    });
  }

  //
/*   addmanager(projectManager){

     this.projectApi.addProjectManager(this.projectManager)
       .subscribe(data => {

         this.projectApi.showMessage(Object.values(data), Object.keys(data))
       });
     this.projectListSubs = this.projectApi
       .getProjects()
       .subscribe(res => {
         this.project_list = res;
         this.copyProjList = res
       },

       );
     this.router.navigate(['/project']);
     this.router.routeReuseStrategy.shouldReuseRoute = () => false;
     this.router.onSameUrlNavigation = 'reload';
     this.router.navigate(['/project']);
    }
   open1(contentPM,project_code ) {
     this.projectManager.project_id = project_code;

     this.modalService.open(contentPM, { ariaLabelledBy: 'modal-basic-title' }).result.then((result) => {
       this.closeResult = `Closed with: ${result}`;

       console.log("Project Manager", this.projectManager);
       this.addmanager(this.projectManager);
     }, (reason) => {
       this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;

     });
   }  */


  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
  applyFilter() {
    let { selectedProject, projectID, clientName } = this.dataForFilter

    this.project_list = this.copyProjList.filter(item =>
      (item['project_code'] === projectID || projectID === "All") &&
      (item['project_name'] === selectedProject || selectedProject === "All") &&
      (item['client_name'] === clientName || clientName === "All")
    )
    Object.entries(this.dataForFilter).map(([key, value]) => {
      this.dataForFilter[key] = 'All'
    })
  }

  resetFilter() {
    Object.entries(this.dataForFilter).map(([key, value]) => {
      this.dataForFilter[key] = 'All'
    })
  }
  openFilter() {

  }
  searchData() {
    if (this.searchInput == "") {
      this.project_list = this.copyProjList.map(item => { return item })
      return this.project_list
    }
    this.project_list = this.copyProjList.filter(res => {
     return  res.project_name.toLocaleLowerCase().match(this.searchInput.toLocaleLowerCase())
        || res.project_code.toLocaleLowerCase().match(this.searchInput.toLocaleLowerCase())
        || res.client_name.toLocaleLowerCase().match(this.searchInput.toLocaleLowerCase())
    })
  }
}
