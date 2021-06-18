import { Component, OnInit, Input } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from "@angular/router";
import { CalendarOptions } from '@fullcalendar/angular'; // useful for typechecking
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
      if (config) {
         this.defaultConfigurations = config;
      }
   }
   
   calendarOptions: CalendarOptions = {
      initialView: 'dayGridMonth',  
      dateClick: this.onDateClick.bind(this),
      
   };
   
    onDateClick(res) {
      alert('Clicked on date : ' + res.dateStr)
    }

   constructor(private router: Router, private cookieService: CookieService) {}
   ngOnInit(): void {
      if (this.cookieService.get('login') == 'true') { }
      else {
         this.router.navigate(['/login']);
      }
   }

}
