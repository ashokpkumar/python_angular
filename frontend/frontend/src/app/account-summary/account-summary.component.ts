import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {userInfo,userData} from './account';
import {accountService} from './account.service';
@Component({
  selector: 'app-account-summary',
  templateUrl: './account-summary.component.html',
  styleUrls: ['./account-summary.component.css']
})
export class AccountSummaryComponent implements OnInit {
  public personal:boolean = false;
  public professional:boolean = false;
  public time:boolean = false;

  userInfo = new userInfo();
  userData = new userData()

  constructor(private apiService:accountService,private cookieService: CookieService) { }
  ngOnInit(): void {
    this.userInfo.emp_id = this.cookieService.get('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{console.log("Employee Data: ",data),
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.professional = true;
    this.personal = false;
    this.time = false;
  }
  openNav(){
    console.log("Menu is being clicked");
    document.getElementById("mySidenav").style.width="250px";
    document.getElementById("main").style.marginLeft="250px";

  }
  closeNav(){
    console.log("Menu is being clicked");
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";

  }
  personalShow(){
    this.professional = false;
    this.personal = true;
    this.time = false;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  professionalShow(){
    this.professional = true;
    this.personal = false;
    this.time = false;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  timeShow(){
    this.professional = false;
    this.personal = false;
    this.time = true;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  logout(){
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
 

}
