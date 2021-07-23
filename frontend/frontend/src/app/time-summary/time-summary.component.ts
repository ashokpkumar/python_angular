import { Component, OnInit, TemplateRef } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import { CalendarOptions } from '@fullcalendar/angular';
import {userInfo,userData,timeinfo} from './timeInfo';
import {TimesummaryService} from './time-summary.service'
import { HttpClient } from '@angular/common/http';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { ViewChild } from '@angular/core';
import { from } from 'rxjs';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction'; 


@Component({
  selector: 'app-time-summary',
  templateUrl: './time-summary.component.html',
  styleUrls: ['./time-summary.component.css']
})
export class TimeSummaryComponent implements OnInit {
  //calendarOptions: CalendarOptions;
  posts = [];
  data = {};
  public time:boolean = false;
  userInfo = new userInfo();
  userData = new userData();
  timeInfo = new timeinfo();
  view: string = 'month';
  todaysDate:any;
  viewDate: Date = new Date();
  spec=`optionValue`;
  project_id:any
  

  public show:boolean = false;
  public buttonName:any = 'Show';
  calendarPlugins = [dayGridPlugin, interactionPlugin];


  constructor(private router: Router,private modalService: NgbModal,private apiService: TimesummaryService,private http: HttpClient,private cookieService: CookieService) { }
  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;
  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
    this.userInfo.emp_id = this.cookieService.get('username');
    this.apiService.onSubmit(this.userInfo)
    .subscribe(data=>{console.log("Employee Data: ",data),
    this.userData = data,
    this.apiService.showMessage(Object.values(data),Object.keys(data))});

    this.time=false;

    setTimeout(() => {
      return this.apiService.getEvents().subscribe(res=>{
        console.log("Result",res);
        for (let value of res){
          //console.log("Iteration",value)
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
  

  calendarOptions: CalendarOptions = {
    initialView: 'dayGridMonth',
    dateClick: this.handleDateClick.bind(this), // bind is important!

  };
  
  timeShow(){
    this.time = true;
    console.log("Time Show");
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }
  handleDateClick(arg) {
    //alert('date click! ' + arg.dateStr)
    this.timeInfo.date = arg.dateStr;
    this.open(this.defaultTabButtonsTpl);
    this.todaysDate=arg.dateStr
  
  }
  open(content) {

    this.modalService.open(this.defaultTabButtonsTpl, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      console.log("Time Info",this.timeInfo);
      this.timeInfo['user_id']=this.cookieService.get('username');;
      this.timeInfo['manager_name']=this.userData.manager_id ;
      this.project_id=this.timeInfo.project_id

      this.apiService.addTimeSubmissions(this.timeInfo)
      .subscribe(data=>{console.log("Employee Data: ",data),
      this.userData = data,
      console.log(data)
      this.apiService.showMessage(Object.values(data),Object.keys(data)),
      this.timeShow();
      this.apiService.getEvents().subscribe(res=>{    console.log("146",res)        
        for (let value of res){this.posts.push(value);}
      },) ;
      this.timeShow();
  
    });
  
      
      }, (reason) => {
  
      });
    }

    toggle() {
      this.show = !this.show;
  
      //CHANGE THE NAME OF THE BUTTON.
      if(this.show)  
        this.buttonName = "Hide";
      else
        this.buttonName = "Show";
    }
    
}
