import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {timeSubmissionsService} from './timesubmissions.service';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-timesubmissions',
  templateUrl: './timesubmissions.component.html',
  styleUrls: ['./timesubmissions.component.css']
})
export class TimesubmissionsComponent implements OnInit {
  submissionList = [];
  faCheck = faCheck;
  faTimes = faTimes;
  user_name : String;
  constructor(private router: Router,private cookieService: CookieService, private apiService:timeSubmissionsService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.user_name = "i3228";
    this.apiService.getSubmissions(this.user_name)
    .subscribe(data=>{console.log("Employee Data: ",data),
    this.submissionList = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    // this.submissionList = [{'date':'20-04','username':'i3228','managername':'i3228','timetype':'CL','hours':'8'},
    // {'date':'20-04','username':'i3228','managername':'i3228','timetype':'SL','hours':'8'},
    // {'date':'20-04','username':'i3228','managername':'i3228','timetype':'WFH','hours':'4'}
    // ]
  }
  review(reviewd,date,user_id,time_type,hours){
// console.log(reviewd);
//  console.log(date);
//  console.log(user_name);
//  console.log(time_type);
//  console.log(hours);
 this.apiService.reviewSubmission(reviewd,date,user_id,time_type,hours)
 .subscribe(data=>{console.log(data);this.apiService.showMessage(Object.values(data),Object.keys(data))});
 this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  this.router.onSameUrlNavigation = 'reload';
  this.router.navigate(['/timesubmission']);
  }
}
