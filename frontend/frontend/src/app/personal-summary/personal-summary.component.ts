import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {userInfo,userData,timeInfo} from './personal.info';
import { PersonalsummaryService } from './personal.service';
@Component({
  selector: 'app-personal-summary',
  templateUrl: './personal-summary.component.html',
  styleUrls: ['./personal-summary.component.css']
})
export class PersonalSummaryComponent implements OnInit {
  public personal:boolean = false;
  
  userInfo = new userInfo();
  userData = new userData();


  constructor(private router: Router,private apiService: PersonalsummaryService,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (window.sessionStorage.getItem('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.userInfo.emp_id = window.sessionStorage.getItem('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{console.log("Employee Data: ",data),
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.personal=false;
   
  }
  personalShow(){
    this.personal = true;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }

}
