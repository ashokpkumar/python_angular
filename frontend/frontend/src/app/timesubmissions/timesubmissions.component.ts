import { Component, OnInit,TemplateRef ,ViewChild} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {users} from "./timeinfo";
import {timeSubmissionsService} from './timesubmissions.service';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { DatePipe } from '@angular/common';
import {FormControl, FormGroup} from '@angular/forms';

declare var $: any;
@Component({
  selector: 'app-timesubmissions',
  templateUrl: './timesubmissions.component.html',
  styleUrls: ['./timesubmissions.component.css']
})
export class TimesubmissionsComponent implements OnInit {
  submissionList = [];
  submissionClicked :any;
  timeClicked :any;
  faCheck = faCheck;
  faTimes = faTimes;
  user_id : String;
  downloadAs: String = "Summary as Csv";
  timeDatas = [];
  totalTime = {};
  rawData ={};
  modaluser_name:any;
  modaltime_type:any;
  pipe: DatePipe;
  from_Date:any;
  to_Date:any;
  sortDir = 1;//1= 'ASE' -1= DSC



  arr = [];
  allUserUnapproved:boolean;
  allUserapproved:boolean;
  individualUnapproved:boolean;

  public users:any
  roles: any
  isVisible: boolean=false;

  weekendsDatesFilter = (d: Date): boolean => {
    const day = d.getDay();

    /* Prevent Saturday and Sunday for select. */
    return day !== 0 && day !== 6 ;
  }

  constructor(private modalService: NgbModal,private router: Router,private cookieService: CookieService, private apiService:timeSubmissionsService) { }
  @ViewChild('approved')
  private defaultTabButtonsTpl1: TemplateRef<any>;
  
  @ViewChild('unapproved')
  private defaultTabButtonsTpl2: TemplateRef<any>;  
  
  ngOnInit(): void {
    this.allUserUnapproved = false;
    if (this.cookieService.get('login')=='true'){
      this.roles=this.cookieService.get('roles');
      this.checkRoles(this.roles)
    }
    else{
      this.router.navigate(['/login']);
    }
    this.user_id = "I3186";
    // this.user_name = "I3228";
    this.apiService.getSubmissions(this.user_id)
    .subscribe(data=>{
    this.submissionList = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.apiService.getTimeData(this.user_id)
    .subscribe(data=>{
                 this.timeDatas = data.result,
                 this.totalTime = data.total 
                 console.log(data)                 
                    });
  }
  clickNumbers(user,user_name,type){

console.log(user,user_name,type);
if (type=='unapproved'){
  this.apiService.getSubmissionsBy(user)
  .subscribe(data=>{
    this.submissionClicked = data,
    this.open(this.defaultTabButtonsTpl2),
    
    this.allUserUnapproved=true,
    this.allUserapproved=false
    this.modaluser_name=user_name
    this.modaltime_type=type
    
  
  });

}else{
  this.apiService.getTimeBy(user,user_name,type)
  .subscribe(data=>{
    console.log("Employee Data: ",data),
    this.timeClicked = data,
    this.open(this.defaultTabButtonsTpl1),
    this.allUserapproved=true,
    this.allUserUnapproved=false
    this.modaluser_name=user_name
    this.modaltime_type=type
 
  });
}
  }
  review(reviewd,date,user_id,time_type,hours){
 this.apiService.reviewSubmission(reviewd,date,user_id,time_type,hours)
 .subscribe(data=>{console.log(data);this.apiService.showMessage(Object.values(data),Object.keys(data))});
 this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  this.router.onSameUrlNavigation = 'reload';
  this.router.navigate(['/timesubmission']);
  }
  checkRoles(roles) {
    let userRoles = roles.split(",");
    console.log(userRoles);
     for (const role of userRoles) {
       if ( role==users.admin) {
         this.isVisible = true;
       } 
     }
   }
  open(content) {
  console.log(this.timeClicked);
  if (this.timeClicked !=0 && this.submissionClicked !=0){
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
    
    }, (reason) => {

    });
  }
}
raw_data(raw_data){
this.apiService.rawData(raw_data)
.subscribe(data=>{
  this.rawData=data});
}





filterForm = new FormGroup({
    fromDate: new FormControl(),
    toDate: new FormControl(),
});

get fromDate() { return this.filterForm.get('fromDate'); }
get toDate() { return this.filterForm.get('toDate'); }



  getDateRange(value) {
    // getting date from calendar
    const fromDate = value.fromDate
    const toDate = value.toDate

    
    var from_Date = new Date(fromDate);
    var to_Date = new Date(toDate);     
    console.log(getFormattedString(from_Date));
    console.log(getFormattedString(to_Date));
    function getFormattedString(d){
      return d.getFullYear() + "/"+(d.getMonth()+1) +"/"+d.getDate() + ' '+d.toString().split(' ')[4]
    }
    //this.apiService.getTimeData(this.user_id, getFormattedString(from_Date).toString(),getFormattedString(to_Date).toString())
    //.subscribe(data=>{
    //  this.timeDatas =data
    //  console.log(data)
    //  this.apiService.showMessage(Object.values(data),Object.keys(data))});
      
      // this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      // this.router.onSameUrlNavigation = 'reload';
      // this.router.navigate(['/timesubmission']);
  }
    
  download(){
    this.apiService.downloadFile(this.timeDatas, 'jsontocsv');
  }   
  download_approved(){
    this.apiService.download_timeinfo(this.timeClicked, 'jsontocsv');
  } 
  download_unapproved(){
    this.apiService.download_reviewtime(this.submissionClicked, 'jsontocsv'); 
  }
  download_data(raw_data){
    this.apiService.rawData(raw_data)
  .subscribe(data=>{console.log(data)
    this.rawData=data
    console.log(this.rawData)

    this.apiService.download_rawdata(this.rawData , 'jsontocsv'); });
  }
  download_modalApprovedData(){
    this.apiService.download_timeinfoRawData(this.timeClicked, 'jsontocsv');
  }
  download_modalUnapprovedData(){  
    this.apiService.download_reviewtimeRawData(this.timeClicked, 'jsontocsv');
  }

  key:string ='userid';
  reverse:boolean=false;
  sort(key){
    this.key=key;
    this.reverse=!this.reverse;
  }


 
}
