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
import { ChangeDetectionStrategy } from '@angular/core';
  
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
    green: {
      primary: '#2aed0c',
      secondary: '#2aed0c',
    },
  };


@Component({
  selector: 'app-time-summary',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './time-summary.component.html',
  styleUrls: ['./time-summary.component.css']
})

export class TimeSummaryComponent implements OnInit {
  
  // @ViewChild('modalContent', { static: true }) modalContent: TemplateRef<any>;
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
  date:any
  

  public show:boolean = false;
  public buttonName:any = 'Show';
  viewDate: Date = new Date();
  view: CalendarView = CalendarView.Month;
  CalendarView = CalendarView;


  modalData: {
    action: string;
    event: CalendarEvent;
  };

  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;
  // constructor(private router: Router,private modalService: NgbModal,private apiService: TimesummaryService,private http: HttpClient,private cookieService: CookieService) { }
  ngOnInit(): void {
   
    if (this.cookieService.get('login')=='true'){
      this.roles=this.cookieService.get('roles');
      this.user_id=this.cookieService.get('username')
      // this.checkRoles(this.roles)
    }
    else{      this.router.navigate(['/login']);   }
    this.getUserData(this.user_id);
  this.getEvents();
  // this.addEvent();
  this.dayClicked(this.date);
  // this.refresh_page(this.date);
 

  }
  @ViewChild('modalContent', { static: true }) modalContent: TemplateRef<any>;


  actions: CalendarEventAction[] = [
    {
      label: '<i class="fas fa-fw fa-pencil-alt"></i>',
      a11yLabel: 'Edit',
      onClick: ({ event }: { event: CalendarEvent }): void => {
        this.handleEvent('Edited', event);
      },
    },
    {
      label: '<i class="fas fa-fw fa-trash-alt"></i>',
      a11yLabel: 'Delete',
      onClick: ({ event }: { event: CalendarEvent }): void => {
        this.events = this.events.filter((iEvent) => iEvent !== event);
        this.handleEvent('Deleted', event);
      },
    },
  ];

  refresh: Subject<any> = new Subject();

  events: CalendarEvent[] = [
  
  ];

  activeDayIsOpen: boolean = false;

  getUserData(user_id){
    this.apiService.getUserInfo(user_id)
    .subscribe(data=>{
      
      this.userData.project_code = data.project_code.split(",");
     
    })
  }

  refresh_page({ date, events }: { date: Date; events: CalendarEvent[] }): void {
  
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
  }
  getFormattedString(d){
    return d.getDate() + "/"+(d.getMonth()+1) +"/"+ d.getFullYear() + ' '+d.toString().split(' ')[4]
  }
  constructor(private router: Router,private modalService: NgbModal,private apiService: TimesummaryService,private http: HttpClient,private cookieService: CookieService) { }

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

   
    this.date1=this.getFormattedString(date)
  
    this.timeInfo.date = this.date1.split(" ")[0];
    this.open1(this.defaultTabButtonsTpl);
    this.todaysDate=this.getFormattedString(date)
  }

  eventTimesChanged({
    event,
    newStart,
    newEnd,
  }: CalendarEventTimesChangedEvent): void {
    this.events = this.events.map((iEvent) => {
      if (iEvent === event) {
        return {
          ...event,
          start: newStart,
          end: newEnd,
        };
      }
      return iEvent;
    });
    this.handleEvent('Dropped or resized', event);
  }

  handleEvent(action: string, event: CalendarEvent): void {
  
    this.modalData = { event, action };
    this.modalService.open(this.modalContent, { size: 'lg' });
  }

  getEvents(): void {
    this.apiService.getEvents()
    .subscribe(data=>{
                 for (let value of data){
                   if (value.status=="unapproved"){
                    value.color=colors.yellow
                   }
                   if (value.status=="approved"){
                    value.color=colors.green
                   }
                   if (value.status=="rejected"){
                    value.color=colors.red
                   }

               
                  value.start = startOfDay(new Date(value.start))

                 }
                 this.events = data;
                    });


  }

  deleteEvent(eventToDelete: CalendarEvent) {
    this.events = this.events.filter((event) => event !== eventToDelete);
  }

  setView(view: CalendarView) {
    this.view = view;
  }

  closeOpenMonthViewDay() {
    this.activeDayIsOpen = false;
  }
  open1(content) {
    this.modalService.open(this.defaultTabButtonsTpl, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
  
      this.timeInfo['user_id']=this.cookieService.get('username');;
      this.timeInfo['manager_id']=this.userData.manager_id ;
      this.project_id=this.timeInfo.project_id

      this.apiService.addTimeSubmissions(this.timeInfo)
      .subscribe(data=>{
      this.userData = data,
    
      this.apiService.showMessage(Object.values(data),Object.keys(data)),
      this.router.onSameUrlNavigation = 'reload';
      // this.timeShow();
      this.apiService.getEvents().subscribe(res=>{          
        for (let value of res){this.posts.push(value);}
      },) ;
      // this.timeShow();
  
    });
  
      
      }, (reason) => {
  
      });
    }
    
}
