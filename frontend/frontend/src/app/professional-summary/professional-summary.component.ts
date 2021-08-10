import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {userData,userInfo,timeInfo} from "./professionalinfo"
import { professionalService } from './personal-summary.service';
@Component({
  selector: 'app-professional-summary',
  templateUrl: './professional-summary.component.html',
  styleUrls: ['./professional-summary.component.css']
})
export class ProfessionalSummaryComponent implements OnInit {
  posts = [];
  data = {};
  
  public personal:boolean = false;
  public professional:boolean = false;
  public time:boolean = false;

  userInfo = new userInfo();
  userData = new userData();
  timeInfo = new timeInfo();

  constructor(private router: Router,private cookieService: CookieService , private apiService:professionalService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.userInfo.emp_id = this.cookieService.get('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.professional = true;
  }
  professionalShow(){
    this.professional = true;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }

}
