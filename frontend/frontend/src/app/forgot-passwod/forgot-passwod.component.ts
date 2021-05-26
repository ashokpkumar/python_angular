import { Component, OnInit } from '@angular/core';
import {ForgotPassService } from './forgot-pass.service';
import {loginService} from '../login/login.service';
import {Router} from "@angular/router";
import {  FormGroup,FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-forgot-passwod',
  templateUrl: './forgot-passwod.component.html',
  styleUrls: ['./forgot-passwod.component.css']
})
export class ForgotPasswodComponent implements OnInit {
  error:any;
  employee_email:any
  constructor(
    private apiServices:ForgotPassService, private router: Router, private apiService:loginService,
  ) {


  }

  ngOnInit(): void {
  }
  forgetpass(value){
    this.apiServices.forgetPass(value)
    .subscribe(data=>{
    if (data.error){
    alert(data.error)
    }
    else{alert("email sent successfully")
    this.router.navigate(['/']);}
    })
  }
}



