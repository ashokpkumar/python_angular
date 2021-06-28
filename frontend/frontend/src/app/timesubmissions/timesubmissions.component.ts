import { Component, OnInit,TemplateRef ,ViewChild} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {users} from "./timeinfo";
import {timeSubmissionsService} from './timesubmissions.service';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';

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
  fromDate:any;
  toDate:any;
  modaluser_name:any;
  modaltime_type:any


  arr = [];
  allUserUnapproved:boolean;
  allUserapproved:boolean;
  individualUnapproved:boolean;

  public users:any
  roles: any
  isVisible: boolean=false;

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
  applyFilter(fromDate,toDate){
    console.log(this.fromDate)
    this.apiService.getSubmissionByDate(fromDate,toDate)
    .subscribe(data=>{console.log(data);this.apiService.showMessage(Object.values(data),Object.keys(data))});
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate(['/timesubmission']);
      }
    
}
