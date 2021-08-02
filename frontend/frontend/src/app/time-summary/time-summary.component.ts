import { Component, OnInit, TemplateRef } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router"
import {userInfo,userData,timeinfo, users} from './timeInfo';
import {TimesummaryService} from './time-summary.service'
import { HttpClient } from '@angular/common/http';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { ViewChild } from '@angular/core';
import { CalendarEventAction, CalendarEventTimesChangedEvent, CalendarView } from 'angular-calendar';
import { CalendarEvent } from 'angular-calendar';
import { from, Subject } from 'rxjs';
import {   startOfDay,
  endOfDay,
  subDays,
  addDays,
  endOfMonth,
  isSameDay,
  isSameMonth,
  addHours, } from 'date-fns';
  
  const colors: any = {
    red: {
      primary: '#ad2121',
      secondary: '#FAE3E3',
    },
    blue: {
      primary: '#1e90ff',
      secondary: '#D1E8FF',
    },
    yellow: {
      primary: '#e3bc08',
      secondary: '#FDF1BA',
    },
  };


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
  view1: string = 'month';
  todaysDate:any;
  spec=`optionValue`;
  project_id:any
  public users:any
  roles: any
  isVisible: boolean=false;
  user_id:any;
  date1:any
  

  public show:boolean = false;
  public buttonName:any = 'Show';
  viewDate: Date = new Date();
  view: CalendarView = CalendarView.Month;
  CalendarView = CalendarView;



  constructor(private router: Router,private modalService: NgbModal,private apiService: TimesummaryService,private http: HttpClient,private cookieService: CookieService) { }
  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;
  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){
      this.roles=this.cookieService.get('roles');
      this.user_id=this.cookieService.get('username')
      this.checkRoles(this.roles)
    }
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
      //if (this.userInfo.emp_id==this.user_id) {}
       return this.apiService.getEvents().subscribe(res=>{
         console.log("Result",res);
         for (let value of res){
           //console.log("Iteration",value)
           this.posts.push(value);
         }
 
       },console.error) ;
    
  
     }, 2000);
    //  setTimeout(() => {
    //    this.events = {
    //    view1: string = 'month';,
    //    dateClick: this.dayClicked.bind(this), // bind is important!
    //    events: this.posts
    //    };
    //  }, 3000);
  }

  
  setView(view: CalendarView) {
    this.view = view;
  }
  addEvent(): void {
    this.events = [
      ...this.events,
      this.dayClicked.bind(this), // bind is important!
      this.events= this.posts,
      {
        title:this.timeInfo.time_type,
        start: startOfDay(new Date()),
        end: endOfDay(new Date()),
        draggable: true,
        resizable: {
          beforeStart: true,
          afterEnd: true,
        },
      },
    ];
  }

  refresh: Subject<any> = new Subject();

  events: CalendarEvent[] = [
    {
      start: subDays(startOfDay(new Date()), 1),
      end: addDays(new Date(), 1),
      title: 'A 3 day event',
      color: colors.red,
      allDay: true,
      resizable: {
        beforeStart: true,
        afterEnd: true,
      },
      draggable: true,
    },
    {
      start: startOfDay(new Date()),
      title: 'An event with no end date',
      color: colors.yellow,
    },
    {
      start: subDays(endOfMonth(new Date()), 3),
      end: addDays(endOfMonth(new Date()), 3),
      title: 'A long event that spans 2 months',
      allDay: true,
    },
    {
      start: addHours(startOfDay(new Date()), 2),
      end: addHours(new Date(), 2),
      title: 'A draggable and resizable event',
      color: colors.yellow,
      resizable: {
        beforeStart: true,
        afterEnd: true,
      },
      draggable: true,
    },
  ];

  activeDayIsOpen: boolean = true;
  

  closeOpenMonthViewDay() {
    this.activeDayIsOpen = false;
  }

  getFormattedString(d){
    return d.getDate() + "/"+(d.getMonth()+1) +"/"+ d.getFullYear() + ' '+d.toString().split(' ')[4]
  }
  
  dayClicked({ date, events }: { date: Date; events: CalendarEvent[] }): void {
    if (isSameMonth(date, this.viewDate)) {
      if (
        (isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
        events.length === 0
      ) {
        this.activeDayIsOpen = false;
      } else {
        this.activeDayIsOpen = true;
      }
      this.viewDate = date;
    }
    console.log(date);
    //this.openAppointmentList(date)
    this.date1=this.getFormattedString(date)
    console.log(this.date1.split(" ")[0])
    this.timeInfo.date = this.date1.split(" ")[0];
    this.open(this.defaultTabButtonsTpl);
    this.todaysDate=this.getFormattedString(date)
  }
  timeShow(){
    this.time = true;
    console.log("Time Show");
    document.getElementById("mySidenav").style.width="0px";
    document.getElementById("main").style.marginLeft="0px";
  }

  checkRoles(roles) {
    let userRoles = roles.split(",");
    console.log(userRoles);
     for (const role of userRoles) {
       if ( role==users.employees,users.manager,users.projectManager) {
         this.isVisible = true;
       } 
     }
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

    
}
