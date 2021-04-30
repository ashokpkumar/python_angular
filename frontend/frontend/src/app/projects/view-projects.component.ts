//https://ng-bootstrap.github.io/#/components/modal/examples

import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { projectsApiService } from './projects.services';
import { CookieService } from 'ngx-cookie-service';
import { Router } from "@angular/router"
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { projectResource } from './assign';
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

  public project_list: any;
  public employee_list: any;
  public copyProjList: any
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
      this.projectListSubs = this.projectApi
        .getProjects()
        .subscribe(res => {
          this.project_list = res;
          this.copyProjList = res
          console.table(res)
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
