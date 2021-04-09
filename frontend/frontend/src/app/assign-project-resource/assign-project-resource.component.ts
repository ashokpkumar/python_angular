import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

@Component({
  selector: 'app-assign-project-resource',
  templateUrl: './assign-project-resource.component.html',
  styleUrls: ['./assign-project-resource.component.css']
})
export class AssignProjectResourceComponent implements OnInit {

  constructor(private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='false')
    {this.router.navigate(['/login']); }
  }

}
