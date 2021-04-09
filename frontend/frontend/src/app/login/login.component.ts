import { Component, OnInit } from '@angular/core';
import {login} from './login';
import {loginService} from './login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  project = new login();
  constructor(private apiService:loginService) { }

  ngOnInit(): void {
  }
  onSubmit() {
    this.apiService.addProject(this.project)
    .subscribe(data=>{console.log(data)})
    console.log(this.project);
  }

}
