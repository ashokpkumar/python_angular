import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
@Component({
  selector: 'app-time-summary',
  templateUrl: './time-summary.component.html',
  styleUrls: ['./time-summary.component.css']
})
export class TimeSummaryComponent implements OnInit {

  constructor(private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
  }

}
