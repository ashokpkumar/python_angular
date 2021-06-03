import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {FormGroup, FormControl} from '@angular/forms';
import {showTimeApiService} from './showtime.service';
import {userInfo,userData} from './time';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

declare var $: any;

@Component({
  selector: 'app-show-time',
  templateUrl: './show-time.component.html',
  styleUrls: ['./show-time.component.css']
})
export class ShowTimeComponent implements OnInit {
  userInfo = new userInfo();
  userData = new userData()
  roles: any
  isVisible: boolean=true;

  constructor(private router: Router,private cookieService: CookieService,private apiService:showTimeApiService, private modalService: NgbModal) {
    
   }
  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;
  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){
      this.roles=this.cookieService.get('roles');
      this.checkRoles(this.roles)
    }
    else{
      this.router.navigate(['/login']);
    }
    this.userInfo.emp_id = this.cookieService.get('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{console.log("Employee Data: ",data),
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});
 
  }
 clickButton(){
  this.modalService.open(this.defaultTabButtonsTpl, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {

  }, (reason) => {

  });
 }
 checkRoles(roles) {
  let userRoles = roles.split(",");
  console.log(userRoles);
   for (const role of userRoles) {
     if ( role=="Admin") {
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
}
