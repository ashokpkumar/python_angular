import { Component, OnInit } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

@Component({
  selector: 'app-assign-resource-project',
  templateUrl: './assign-resource-project.component.html',
  styleUrls: ['./assign-resource-project.component.css']
})
export class AssignResourceProjectComponent implements OnInit {

  constructor(private router: Router,private cookieService: CookieService) { }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='false')
    {this.router.navigate(['/login']); }
  }

}
