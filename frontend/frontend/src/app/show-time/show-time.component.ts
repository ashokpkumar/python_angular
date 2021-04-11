import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { CalendarOptions } from '@fullcalendar/angular'; 
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {FormGroup, FormControl} from '@angular/forms';

declare var $: any;

@Component({
  selector: 'app-show-time',
  templateUrl: './show-time.component.html',
  styleUrls: ['./show-time.component.css']
})
export class ShowTimeComponent implements OnInit {


  calendarOptions: CalendarOptions = {
    initialView: 'dayGridMonth',
    dateClick: this.handleDateClick.bind(this), // bind is important!
    events: [
      { title: 'event 1', date: '2020-06-27' },
      { title: 'event 2', date: '2020-06-30' }
    ]
  };
  constructor(private modalService: NgbModal) {

    const today = new Date();
    const month = today.getMonth();
    const year = today.getFullYear();

    
   }
  @ViewChild('content')
  private defaultTabButtonsTpl: TemplateRef<any>;
  ngOnInit(): void {
   
 
  }
  handleDateClick(arg) {
    console.log("Date clicked ",arg.dateStr);
    //this.projectResource.project_id = project_code;
    // console.log('Project Code: ',project_code);
    this.modalService.open(this.defaultTabButtonsTpl, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      //this.closeResult = `Closed with: ${result}`;
      // console.log(this.closeResult);
       //console.log("Project resource",this.projectResource);
      //this.addResource(this.projectResource);
    }, (reason) => {
      //this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
      // console.log(this.closeResult);
      // console.log(this.projectResource);
    });
  }
  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
}
