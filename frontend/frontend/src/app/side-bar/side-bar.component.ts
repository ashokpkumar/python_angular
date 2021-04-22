import { Component, OnInit } from '@angular/core';
import { faChevronRight,faChevronDown} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.css']
})
export class SideBarComponent implements OnInit {
  faChevronRight = faChevronRight
  faChevronDown =faChevronDown
  dropDownList = {employeeDropDownList:false,projectDropDownList:false}
  constructor() { 
  }

  ngOnInit(): void {
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
