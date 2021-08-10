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
    
    if(this.cookieService.get('login')=='true'){
        this.login=true;
    }else{
        this.login=false;
    }

  }
  createPassword(){
    this.apiService.setPassword(this.project)
    .subscribe(data=>{
      this.router.navigate(['/']);
      this.login=false;
      this.apiService.showMessage(Object.values(data),Object.keys(data));
    },
                err=>{console.log(err);});

      }
  onSubmit() {
   
    this.apiService.addProject(this.project)
    .subscribe(data=>
      
      {
        
      if (Object.keys(data).indexOf('error')>-1){
          
          this.apiService.showMessage(Object.values(data),Object.keys(data))

      }
      else if(Object.keys(data).indexOf('access_token')>-1){
        
        this.apiService.showMessage('Welcome : ' + data['employee_name'],'success');
       
        this.cookieService.set('access_token',data['access_token']);
        this.cookieService.set('username',data['username']);
        this.cookieService.set('roles',data['roles']);
        this.cookieService.set('login',data['login']);
    
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['/']);
      }
      
      else if(Object.keys(data).indexOf('warning')>-1){
        this.apiService.showMessage(Object.values(data),Object.keys(data));
        this.forgotPass=true;
      }
    })
 
  }
  logout(){
    this.cookieService.set('login','false');

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
