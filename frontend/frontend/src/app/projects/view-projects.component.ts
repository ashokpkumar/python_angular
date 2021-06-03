//https://ng-bootstrap.github.io/#/components/modal/examples

import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { projectsApiService } from './projects.services';
import { CookieService } from 'ngx-cookie-service';
import { Router } from "@angular/router"
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { projectResource } from './assign';
import { projectManager } from './assignPM';
import {ResourceList} from './Resourcelist';
import { FormControl } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { faSearch, faSlidersH, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import { NgxBootstrapIconsModule } from 'ngx-bootstrap-icons';
@Component({
  selector: 'app-view-projects',
  templateUrl: './view-projects.component.html',
  styleUrls: ['./view-projects.component.css']
})
export class ViewProjectsComponent implements OnInit {
  projectResource = new projectResource();
  projectManager = new projectManager();
  ResourceList= new ResourceList();

  public project_list: any;
  public employee_list: any;
  public project_resource_list: any;
  public copyProjList: any
  public copyEmpList: any
  public show:boolean = false;
  public buttonName:any = 'Show';

  project_name: any
  project_id: any
  client_name: any

  projectListSubs: Subscription;
  searchInput:String;
  searchInputName:String;
  projectCodeRemoval:String;
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
  addResourceList(ResourceList){
    this.projectApi.getResourceInfo(this.ResourceList)
    .subscribe(data => {

      this.projectApi.showMessage(Object.values(data), Object.keys(data))
    });
    this.projectListSubs = this.projectApi
      .getProjects()
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

  removeResource(emp_id){
    console.log(emp_id)
    console.log(this.projectCodeRemoval)
    this.projectListSubs = this.projectApi.removeProjectResource(emp_id,this.projectCodeRemoval)
    .subscribe(res => {});

  }
  openRL(contentRL, project_code) {
this.projectCodeRemoval = project_code
    this.projectListSubs = this.projectApi    .getResourceInfo(project_code)
    .subscribe(res => {
      this.project_resource_list = res
      console.log(res)
   this.modalService.open(contentRL, { ariaLabelledBy: 'modal-basic-title' }).result.then((result) => {
    this.closeResult = `Closed with: ${result}`;

    console.log("Project resource", this.projectResource);
    this.addResource(this.projectResource);
  }, (reason) => {
    this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;

  });
    }

    

    );
  
  }
    
  
    

    /*   openRL(contentRL, resource_info){
    this.ResourceList.resource_id= resource_info;
  } */



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
  searchEmp(){
    if (this.projectResource.first_name == ""){
      this.employee_list=this.copyEmpList.map(item =>{return item})
      return this.employee_list
    }
    this.employee_list=this,this.copyEmpList.filtr(res=>{
      return res.first_name.toLocaleLowerCase().match(this.projectResource.first_name.toLocaleLowerCase())
    })
  }
  toggle() {
    this.show = !this.show;

    // CHANGE THE NAME OF THE BUTTON.
    if(this.show)  
      this.buttonName = "Hide Info";
    else
      this.buttonName = "Show Info";
  }
  chosenemp: string = "";

info(){
  if(this.chosenemp) { 
    this.show = this.show;
     }
  }

}
