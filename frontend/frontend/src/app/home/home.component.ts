import { Component, OnInit } from '@angular/core';

import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import { faSearch, faBell, faUser, faCoffee,faHome,faAddressCard,faToolbox,faTools,faClock} from '@fortawesome/free-solid-svg-icons';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  faSearch = faSearch;
  faBell = faBell;
  faUser = faUser;
  faCoffee  = faCoffee ;
  faHome = faHome;
  faAddressCard=faAddressCard;
  faToolbox=faToolbox;
  faTools=faTools;
  faClock=faClock;
  constructor(private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
  }

}
