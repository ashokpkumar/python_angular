import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-timesubmissions',
  templateUrl: './timesubmissions.component.html',
  styleUrls: ['./timesubmissions.component.css']
})
export class TimesubmissionsComponent implements OnInit {
  submissionList = []
  constructor() { }

  ngOnInit(): void {
    this.submissionList = [{'date':'20-04','username':'i3228','managername':'i3228','timetype':'CL','hours':'8'},
    {'date':'20-04','username':'i3228','managername':'i3228','timetype':'SL','hours':'8'},
    {'date':'20-04','username':'i3228','managername':'i3228','timetype':'WFH','hours':'4'}
    ]
  }
  review(reviewd){
console.log(reviewd);
// console.log(username)
  }
}
