import { Variable } from '@angular/compiler/src/render3/r3_ast';
import { Component, OnInit } from '@angular/core';
import {Subscription} from 'rxjs';
import { ExamsApiService } from './exams.service';


@Component({
  selector: 'app-exams',
  templateUrl: './exams.component.html',
  styleUrls: ['./exams.component.css']
})
export class ExamsComponent implements OnInit {
  public examsList: any;
  examsListSubs: Subscription;
  constructor(private examsApi: ExamsApiService) { }

  ngOnInit(){
    
    this.examsListSubs = this.examsApi
    .getExams()
    .subscribe(res => {
        this.examsList = res;
      },
      console.error
    );

    console.log("This is Exam", this.examsList);
  }

}
