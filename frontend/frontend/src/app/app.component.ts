import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs'
import {CookieService} from 'ngx-cookie-service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  [x: string]: any;
  title = 'frontend';
  examsListSubs: Subscription;
  isVisible: boolean=false;
  
  constructor(private cookieService: CookieService,){}
  
  ngOnInit() {
    if (window.sessionStorage.getItem('login')=='true'){
      this.isVisible=true
    }
  }

  ngOnDestroy() {
    this.examsListSubs.unsubscribe();
  }

}
