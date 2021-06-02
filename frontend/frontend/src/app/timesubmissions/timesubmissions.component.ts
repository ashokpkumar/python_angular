import { Component, OnInit,TemplateRef ,ViewChild} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
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
  user_name : String;
  downloadAs: String = "Summary as Csv";
  timeDatas = [];
  totalTime = {};

  arr = [];
  allUserUnapproved:boolean;
  allUserapproved:boolean;
  individualUnapproved:boolean;

  roles: any
  isVisible: boolean=true;

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
    this.user_name = "I3186";
    // this.user_name = "I3228";
    this.apiService.getSubmissions(this.user_name)
    .subscribe(data=>{
    this.submissionList = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.apiService.getTimeData(this.user_name)
    .subscribe(data=>{
                 this.timeDatas = data.result,
                 this.totalTime = data.total                  
                    });
  }
  clickNumbers(user,type){

console.log(user,type);
if (type=='unapproved'){
  this.apiService.getSubmissionsBy(user)
  .subscribe(data=>{
    this.submissionClicked = data,
    this.open(this.defaultTabButtonsTpl2),
    
    this.allUserUnapproved=true,
    this.allUserapproved=false
  });

}else{
  this.apiService.getTimeBy(user,type)
  .subscribe(data=>{
    console.log("Employee Data: ",data),
    this.timeClicked = data,
    this.open(this.defaultTabButtonsTpl1),
    this.allUserapproved=true,
    this.allUserUnapproved=false
 
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
       if ( role=="RMG Admin" || role=="Employee") {
         this.isVisible = true;
       } else  {
         this.isVisible = false;
       }
     }
   }

  open(content) {
  console.log(this.timeClicked);
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      

    
    }, (reason) => {

    });
  }
}
