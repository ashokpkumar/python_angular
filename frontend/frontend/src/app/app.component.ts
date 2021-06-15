import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs'
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'frontend';
  examsListSubs: Subscription;

  currentRoute: string;
  constructor(private router: ActivatedRoute) {

  }

  ngAfterViewChecked() {
    this.currentRoute = this.router['_routerState']['snapshot']['url']
  }
  ngOnInit() {
    this.currentRoute = this.router['_routerState']['snapshot']['url']
  }
  ngOnDestroy() {
    this.examsListSubs.unsubscribe();
  }

}
