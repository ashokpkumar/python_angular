import { Component, OnInit } from '@angular/core';
import { faChevronRight,faChevronDown} from '@fortawesome/free-solid-svg-icons';
import {CookieService} from 'ngx-cookie-service';
import { ToastrService } from 'ngx-toastr';
import {Router} from "@angular/router";

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.css']
})
export class SideBarComponent implements OnInit {
  faChevronRight = faChevronRight
  faChevronDown =faChevronDown
  dropDownList = {employeeDropDownList:false,projectDropDownList:false}
  constructor(private router: Router,public toastr: ToastrService,private cookieService: CookieService) { }
  login: boolean;
  isVisible: boolean=false;

  logout(){
    console.log("Logging out ")
    this.cookieService.set('login','false');
    
    this.router.navigate(['/login']);
  }

  ngOnInit(): void {
    if(this.cookieService.get('login')=='true'){
      this.login=true;
    }

  }
  employeeDropDown=(value,id)=>{
    this.dropDownList[value] = ! this.dropDownList[value]
    if(this.dropDownList[value]){
      document.getElementById(id).classList.toggle("show");
    }
    else{
      document.getElementById(id).classList.remove("show");
    }
  }
}