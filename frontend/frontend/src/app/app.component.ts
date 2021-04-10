import {Component, OnInit, OnDestroy} from '@angular/core';
//import {Subscription} from 'rxjs/Subscription';
import {Subscription} from 'rxjs'


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'frontend';
  examsListSubs: Subscription;
  
  
  ngOnInit() {
  
  }

  ngOnDestroy() {
    this.examsListSubs.unsubscribe();
  }

}
