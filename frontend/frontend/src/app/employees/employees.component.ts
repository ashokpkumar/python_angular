import { Component, OnInit } from '@angular/core';
import {Subscription} from 'rxjs';
import {employeesApiService} from './employees.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  public employee_list: any;
  empListSubs: Subscription;
  constructor(private empApi: employeesApiService,private router: Router,private cookieService: CookieService) { }

  ngOnInit()  {
    if (this.cookieService.get('login')=='false'){
      this.router.navigate(['/login']);
    }
    this.empListSubs = this.empApi
                            .getExams()
                            .subscribe(res=>{this.employee_list=res;console.log(res)},console.error) ;
  }

}
