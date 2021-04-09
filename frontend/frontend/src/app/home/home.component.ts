import { Component, OnInit } from '@angular/core';
import { faSearch, faBell, faUser,faCoffee  } from '@fortawesome/free-solid-svg-icons';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

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
  constructor(private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='false')
    {this.router.navigate(['/login']); }
  }

}
