import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
 import {timeinfo,userInfo} from './timeInfo';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class TimesummaryService {
  constructor(public toastr: ToastrService,private http: HttpClient) {
  }


  showMessage(message, title){
    if (title=='success'){
        this.toastr.success(message, title)
    }else if (title=='error'){
        this.toastr.error(message, title)
    }
    else if (title=='info'){
        this.toastr.info(message, title)
    }
    else if (title=='warning'){
        this.toastr.warning(message, title)
    }    
} 

  addTimeSubmissions(timeInfo:timeinfo): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(timeInfo);
    console.log(body)
    return this.http.post(`${API_URL}/addtimesubmissions`, body,{'headers':headers})
  }

  getEvents():Observable<any>{
    return this.http.get(`${API_URL}/events`);
  }

 

}
