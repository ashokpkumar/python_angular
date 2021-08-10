import { Component, OnInit , TemplateRef, ViewChild} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {userInfo,userData} from './account';
import {accountService} from './account.service';
import { HttpClient } from '@angular/common/http';
import { CalendarOptions } from '@fullcalendar/angular';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {timeInfo} from './account';
import {Router} from "@angular/router";
declare var $: any;
@Component({
  selector: 'app-account-summary',
  templateUrl: './account-summary.component.html',
  styleUrls: ['./account-summary.component.css']
})

// https://fullcalendar.io/docs/event-colors-demo
export class AccountSummaryComponent implements OnInit {
  posts = [];
  data = {};
  calendarOptions: CalendarOptions;
  
  public personal:boolean = false;
  public professional:boolean = false;
  public time:boolean = false;

  userInfo = new userInfo();
  userData = new userData();
  timeInfo = new timeInfo();
  constructor(private router: Router,private modalService: NgbModal,private http: HttpClient, private apiService:accountService,private cookieService: CookieService) { }
  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.userInfo.emp_id = this.cookieService.get('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{
      
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.professional = true;
    this.personal = false;
    this.time = false;

    setTimeout(() => {
          return this.apiService.getEvents().subscribe(res=>{
          
            for (let value of res){
            
              this.posts.push(value);
            }
 
          },console.error) ;
          this.posts.push({'title':'This is your','start':'2021-04-29'});
          this.posts.push({'title':'This is your','start':'2021-04-21'});
       
     
      }, 2000);
      setTimeout(() => {
        this.calendarOptions = {
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick.bind(this), // bind is important!
        events: this.posts
        };
      }, 3000);
          
      

    

  }

  openNav(){
  
    document.getElementById("mySidenav").style.width="250px";
    document.getElementById("main").style.marginLeft="250px";

  }
  closeNav(){
 
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";

  }
  personalShow(){
    this.professional = false;
    this.personal = true;
    this.time = false;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  professionalShow(){
    this.professional = true;
    this.personal = false;
    this.time = false;
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  timeShow(){
    this.professional = false;
    this.personal = false;
    this.time = true;
 
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  logout(){
    this.cookieService.set('login','false');
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
    this.router.navigate(['/login']);
  }
  handleDateClick(arg) {
    this.timeInfo.date = arg.dateStr;
    this.open(this.defaultTabButtonsTpl);
  }
  open(content) {
  
    this.modalService.open(this.defaultTabButtonsTpl, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
     
      this.timeInfo['user_name']=this.cookieService.get('username');;
      this.timeInfo['manager_name']=this.cookieService.get('username');;

      this.apiService.addTimeSubmissions(this.timeInfo)
    .subscribe(data=>{
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data)),
    this.timeShow();
    this.apiService.getEvents().subscribe(res=>{          
      for (let value of res){this.posts.push(value);}
    },) ;
    this.timeShow();

  });

    
    }, (reason) => {

    });
  }

}
