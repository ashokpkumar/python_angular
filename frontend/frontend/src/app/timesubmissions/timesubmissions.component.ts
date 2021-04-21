import { Component, OnInit,TemplateRef } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {timeSubmissionsService} from './timesubmissions.service';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
declare var $: any;
@Component({
  selector: 'app-timesubmissions',
  templateUrl: './timesubmissions.component.html',
  styleUrls: ['./timesubmissions.component.css']
})
export class TimesubmissionsComponent implements OnInit {
  submissionList = [];
  submissionClicked :any;
  timeClicked :any;
  faCheck = faCheck;
  faTimes = faTimes;
  user_name : String;
  timeDatas = [];
  totalTime = {};

  arr = [];
  allUserUnapproved:boolean;
  allUserapproved:boolean;
  individualUnapproved:boolean;

  constructor(private router: Router,private cookieService: CookieService, private apiService:timeSubmissionsService) { }

  ngOnInit(): void {
    this.allUserUnapproved = false;
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.user_name = "I3186";
    // this.user_name = "I3228";
    this.apiService.getSubmissions(this.user_name)
    .subscribe(data=>{
    this.submissionList = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.apiService.getTimeData(this.user_name)
    .subscribe(data=>{
                 this.timeDatas = data.result,
                 this.totalTime = data.total                  
                    });
  }
  clickNumbers(user,type){

console.log(user,type);
if (type=='unapproved'){
  this.apiService.getSubmissionsBy(user)
  .subscribe(data=>{
    
    this.submissionClicked = data,
    this.allUserUnapproved=true
    this.allUserapproved=false
  });

}else{
  this.apiService.getTimeBy(user,type)
  .subscribe(data=>{
    console.log("Employee Data: ",data),
    this.timeClicked = data,
    this.allUserapproved=true,
    this.allUserUnapproved=false
 
  });
}
  }
  review(reviewd,date,user_id,time_type,hours){
 this.apiService.reviewSubmission(reviewd,date,user_id,time_type,hours)
 .subscribe(data=>{console.log(data);this.apiService.showMessage(Object.values(data),Object.keys(data))});
 this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  this.router.onSameUrlNavigation = 'reload';
  this.router.navigate(['/timesubmission']);
  }
}
