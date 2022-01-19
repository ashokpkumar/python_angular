import { Component, OnInit } from '@angular/core';
import {timeService} from './time.service';
@Component({
  selector: 'app-individual-time',
  templateUrl: './individual-time.component.html',
  styleUrls: ['./individual-time.component.css']
})
export class IndividualTimeComponent implements OnInit {
  user_name : String;
  constructor(private apiService:timeService) { }
  timeDatas = [];
  ngOnInit(): void {
    this.user_name = "I3186";
    this.apiService.getTimeData(this.user_name)
    .subscribe(data=>{console.log("Time Data: ",data),
                 this.timeDatas = data.result,
                   console.log(typeof( this.timeDatas)),
                   console.log(this.timeDatas)


                    
                    });
  }

}
