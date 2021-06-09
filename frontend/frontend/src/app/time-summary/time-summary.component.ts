import { Component, OnInit, Input  } from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import * as $ from 'jquery';
import 'fullcalendar';
import * as moment from 'moment';

@Component({
  selector: 'app-time-summary',
  templateUrl: './time-summary.component.html',
  styleUrls: ['./time-summary.component.css']
})
export class TimeSummaryComponent implements OnInit {

  @Input() eventData: any;
   
   defaultConfigurations: any;

  @Input()
      set configurations(config: any) {
         if(config) {
            this.defaultConfigurations = config;  
         }
      }


  constructor(private router: Router,private cookieService: CookieService) {
    this.defaultConfigurations = {
      editable: true,
               eventLimit: true,
               titleFormat: 'MMM D YYYY',
               header: {
                  left: 'prev,next today',
                  center: 'title',
                  right: 'month,agendaWeek,agendaDay'
               },
               buttonText: {
                  today: 'Today',
                  month: 'Month',
                  week: 'Week',
                  day: 'Day'
               },
               views: {
                  agenda: {
                     eventLimit: 2
                  }
               },
               allDaySlot: false,
               slotDuration: moment.duration('00:15:00'),
               slotLabelInterval: moment.duration('01:00:00'),
               firstDay: 1,
               selectable: true,
               selectHelper: true,
               events: this.eventData,
            };
         
   }

  ngOnInit(): void {
    if (this.cookieService.get('login')=='true'){}
    else{
      this.router.navigate(['/login']);
    }
  }

}
