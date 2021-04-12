import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Subscription} from 'rxjs';
import {accountApiService} from './account.service'

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
  public employee_list: any;
  projectListSubs: Subscription;
  constructor(private projectApi: accountApiService,private cookieService: CookieService) { }

  ngOnInit(): void {
    const allCookies: {} = this.cookieService.getAll();
    console.log(allCookies);
    this.projectListSubs = this.projectApi
      .getEmployeeData()
      .subscribe(res=>{this.employee_list=res;console.log(res); }) ;
  }

}
