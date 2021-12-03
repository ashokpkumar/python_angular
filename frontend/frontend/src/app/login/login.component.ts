import { Component, OnInit } from '@angular/core';
import {login,setpass} from './login';
import {loginService} from './login.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"

//https://www.npmjs.com/package/ngx-show-hide-password

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  project = new login();

  public cookie: string;
  public login: boolean;
  public forgotPass: boolean;
  constructor(private router: Router,
    private apiService:loginService,
    private cookieService: CookieService,
    ) { }

  ngOnInit(): void {
    this.forgotPass=false
    console.log("TOKEN from ngoninit",window.sessionStorage.getItem("access_token"));
    console.log("Username",window.sessionStorage.getItem('username'));
    console.log("roles",window.sessionStorage.getItem('roles'));
    console.log('login',window.sessionStorage.getItem('login'));
    if(window.sessionStorage.getItem('login')=='true'){
        this.login=true;
    }else{
        this.login=false;
    }

  }
  createPassword(){
    this.apiService.setPassword(this.project)
    .subscribe(data=>{console.log(data);
      this.router.navigate(['/']);
      this.login=false;
      this.apiService.showMessage(Object.values(data),Object.keys(data));
    },
                err=>{console.log(err);});

      }
  onSubmit() {
    console.log("Project",this.project)
    this.apiService.addProject(this.project)
    .subscribe(data=>
      
      {
        console.log(data),
      console.log(Object.keys(data));
      console.log(data['error']);
      console.log((Object.keys(data).indexOf('error')>-1));

      if (Object.keys(data).indexOf('error')>-1){
          console.log(data['error'])
          this.apiService.showMessage(Object.values(data),Object.keys(data))

      }
      else if(Object.keys(data).indexOf('access_token')>-1){
        console.log("Coming inside Success",data);
        this.apiService.showMessage('Welcome : ' + data['employee_name'],'success');
        console.log(data["access_token"]);
        console.log(typeof(data["access_token"]));
        window.sessionStorage.setItem('access_token',data['access_token']);
        window.sessionStorage.setItem('username',data['username']);
        window.sessionStorage.setItem('roles',data['roles']);
        window.sessionStorage.setItem('login',data['login']);
        this.router.navigate(['/']);
      }
      
      else if(Object.keys(data).indexOf('warning')>-1){
        this.apiService.showMessage(Object.values(data),Object.keys(data));
        this.forgotPass=true;
      }
    })
    console.log(this.project);
  }
  logout(){
    window.sessionStorage.setItem('login','false');
    console.log("Logged out");
    console.log(window.sessionStorage.getItem('login'));
    this.router.navigate(['/']);
    this.ngOnInit();
    this.apiService.showMessage("You have successfully logged out !","info");
  }
  forgot(){
    this.forgotPass=true;
    this.apiService.showMessage('please set your password here','info')
    this.router.navigate(['/forgotpassword']);
  }

}
