import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {timeData} from './time';
import {Subscription} from 'rxjs';
import {showTimeApiService} from './showtime.service';
@Component({
  selector: 'app-show-time',
  templateUrl: './show-time.component.html',
  styleUrls: ['./show-time.component.css']
})
export class ShowTimeComponent implements OnInit {
  timeData = new timeData();
  projectListSubs: Subscription;
  constructor(private timeApi: showTimeApiService,private modalService: NgbModal,) {

    
   }

  ngOnInit(): void {
   
 
  }
  addResource(content){
console.log(content)

this.projectListSubs = this.timeApi.addProjectResource(content).subscribe(data=>{ this.timeApi.showMessage(Object.values(data),Object.keys(data)); },err=>{this.timeApi.showMessage(Object.values(err),Object.keys(err));} );
  }
  open(content) {
    
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.timeData.manager_name='nataraj';
      this.timeData.user_name = 'i3228';
     this.addResource(this.timeData);
    }, (reason) => {
      
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
