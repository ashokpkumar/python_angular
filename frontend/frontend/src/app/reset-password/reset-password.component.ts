import { Component, OnInit } from '@angular/core';
import {ResetPasswordService } from './reset-password.service';
import {loginService} from '../login/login.service';
import {Router, ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit {
     token: any;
     email: any;

  constructor(private apiServices:ResetPasswordService,  private route: ActivatedRoute, private router: Router, private apiService:loginService,) { }

  ngOnInit(): void {
  this.token = this.route.snapshot.queryParams.token;
   this.email = this.route.snapshot.queryParams.email;
 


  }
   resetPassword(email, password, confirmPass){
   let resetPass ={
   email: email,
   password: password,
   confirm_pass: confirmPass,
   reset_token: this.token
   }
    this.apiServices.resetPassword(resetPass)
    .subscribe(data=>{
      alert("Reset password done");
   
    },
    err => {
    this.router.navigate(['/login']);
    })
  }
}

