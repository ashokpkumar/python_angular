import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { employeesApiService } from './employees.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from "@angular/router";
import { projectResource } from './assign';
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { faSearch, faSlidersH,faTimesCircle } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  public employee_list: any;
  public project_list: any;
  empListSubs: Subscription;
  public copyEmployeeList: any;
  searchInput: String;
  projectListSubs: Subscription;
  projectResource = new projectResource();
  faSearch = faSearch
  faTimesCircle =faTimesCircle
  faSlidersH = faSlidersH
  project_name : any
  project_id : any
  resource_status : any
  manager_name : any
  client_name : any
  delivery_type : any
  roles: any
  isVisible: boolean=true;

  dataForFilter={
    selectedProject:"All",
    projectID:"All",
    resourceStatus:"All",
    managerName:"All",
    clientName:"All",
    deliveryType:"All"
  }

  constructor(private modalService: NgbModal, private empApi: employeesApiService, private router: Router, private cookieService: CookieService) { }

  ngOnInit() {
    let myElement = document.getElementsByClassName("popover") as HTMLCollectionOf<HTMLElement>;
    console.log(myElement);

    if (this.cookieService.get('login') == 'true') {
    this.roles=this.cookieService.get('roles');
    this.checkRoles(this.roles)
  }
    else {
      this.router.navigate(['/login']);
    }
    this.empListSubs = this.empApi
      .getExams()
      .subscribe(res => {
        this.employee_list = res;
        this.copyEmployeeList = res
        let project_name = []
        let project_id = []
        let resource_status = []
        let manager_name = []
        let client_name = []
        let delivery_type = []
        this.employee_list.map(item =>{
          if(item['project_name'] != ""){
            project_name.push(item['project_name'])
          }
          if(item['project_code'] != ""){
            project_id.push(item['project_code'])
          }
          if(item['resource_status'] != ""){
            resource_status.push(item['resource_status'])
          }
          if(item['manager_name'] != ""){
            manager_name.push(item['manager_name'])
          }
          if(item['client_name'] != ""){
            client_name.push(item['client_name'])
          }
          if(item['delivery_type'] != ""){
            delivery_type.push(item['delivery_type'])
          }
        })
        this.project_name= new Set(project_name)
        this.project_id= new Set(project_id)
        this.resource_status = new Set(resource_status)
        this.manager_name = new Set(manager_name)
        this.client_name = new Set(client_name)
        this.delivery_type = new Set(delivery_type)

        console.log(this.employee_list);



      }, console.error);

    this.projectListSubs = this.empApi
      .getProjects()
      .subscribe(res => {
        this.project_list = res;
        console.log(res)
      },
      );
  }
  searchData() {
    console.log(this.searchInput)
    if (this.searchInput == "") {
      this.employee_list = this.copyEmployeeList.map(item => { return item })
      return this.employee_list
    }
    this.employee_list = this.copyEmployeeList.filter(res => {
      return res.full_name.toLowerCase().match(this.searchInput.toLowerCase())
        || res.emp_id.toLowerCase().match(this.searchInput.toLowerCase())
        || res.manager_name.toLowerCase().match(this.searchInput.toLowerCase())
        || res.skills.toLowerCase().match(this.searchInput.toLowerCase())
        || res.project_code.toLowerCase().match(this.searchInput.toLowerCase())
        // || res.client_name.toLowerCase().match(this.searchInput.toLowerCase())
    })
  }
  addResource(projectResource) {
    console.log(projectResource.emp_id);
    console.log(projectResource.project_id);
    this.empApi.addProjectResource(this.projectResource)
      .subscribe(data => {

        this.empApi.showMessage(Object.values(data), Object.keys(data))
      });
    this.router.navigate(['/employee']);
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['/employee']);
  }
  open(content, project_code) {
    this.projectResource.emp_id = project_code;
    console.log('Project Code: ', project_code);
    this.modalService.open(content, { ariaLabelledBy: 'modal-basic-title' }).result.then((result) => {
      this.addResource(this.projectResource);
    }, (reason) => {

    });
  }
  checkRoles(roles) {
   let userRoles = roles.split(",");
   console.log(userRoles);
    for (const role of userRoles) {
      if ( role == "RMG Admin") {
        this.isVisible = true;
      } else  {
        this.isVisible = false;
      }
    }
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
  applyFilter(){
    let {selectedProject,projectID,resourceStatus,managerName,clientName,deliveryType} = this.dataForFilter
      this.employee_list = this.copyEmployeeList.filter(item =>
      ( item['manager_name'] === managerName  || managerName === "All") &&
      ( item['project_code'] === projectID  || projectID === "All") &&
      ( item['resource_status'] === resourceStatus  || resourceStatus === "All") &&
      ( item['project_name'] === selectedProject  || selectedProject === "All") &&
      ( item['client_name'] === clientName  || clientName === "All") &&
      ( item['delivery_type'] === deliveryType  || deliveryType === "All") &&
      ( item['project_name'] === selectedProject  || selectedProject === "All")
     )
     Object.entries(this.dataForFilter).map(([key,value])=>{
      this.dataForFilter[key] = 'All'
    })
  }

  resetFilter(){
    Object.entries(this.dataForFilter).map(([key,value])=>{
      this.dataForFilter[key] = 'All'
    })
  }
  openFilter(){

  }
}
