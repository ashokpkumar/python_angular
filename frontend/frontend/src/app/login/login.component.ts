import { Component, OnInit } from '@angular/core';
import {login} from './login';
import {loginService} from './login.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  project = new login();
  public cookie: string;
  public login: boolean;
  constructor(private router: Router,
    private apiService:loginService,
    private cookieService: CookieService,
    ) { }

  ngOnInit(): void {
    console.log("TOKEN from ngoninit",this.cookieService.get("access_token"));
    console.log("Username",this.cookieService.get('username'));
    console.log("roles",this.cookieService.get('roles'));
    console.log('login',this.cookieService.get('login'));
    if(this.cookieService.get('login')=='true'){
        this.login=true;
    }else{
        this.login=false;
    }
    //this.login=this.cookieService.get('login');
  }
  onSubmit() {
    this.apiService.addProject(this.project)
    .subscribe(data=>{
      console.log(data["access_token"]);
      console.log(typeof(data["access_token"]));
      this.cookieService.set('access_token',data['access_token']);
      this.cookieService.set('username',data['username']);
      this.cookieService.set('roles',data['roles']);
      this.cookieService.set('login',data['login']);
      this.router.navigate(['/']);
    })
    console.log(this.project);
  }
  logout(){
    this.cookieService.set('login','false');
    console.log("Logged out");
    console.log(this.cookieService.get('login'));
    this.router.navigate(['/']);
    this.ngOnInit();
  }

}
