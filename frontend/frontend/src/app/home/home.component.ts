import { Component, OnInit } from '@angular/core';
import { faSearch, faBell, faUser,faCoffee  } from '@fortawesome/free-solid-svg-icons';
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
  constructor() { }

  ngOnInit(): void {
  }

}
