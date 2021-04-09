import { Component, OnInit } from '@angular/core';
import { faSearch, faBell, faUser } from '@fortawesome/free-solid-svg-icons';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {

  private cookieValue: string;

  faSearch = faSearch;
  faBell = faBell;
  faUser = faUser;
  constructor(private cookieService: CookieService) { }

  public ngOnInit(): void {
    this.cookieService.set('cookie-name','our cookie value');
    this.cookieValue = this.cookieService.get('cookie-name');
    console.log("Cookie value", this.cookieValue);
  }

}
