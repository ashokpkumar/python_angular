import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class timeSubmissionsService {
 // 
  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  
  getSubmissions(user_name): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user_name);
    console.log(body)
    return this.http.post(`${API_URL}/view_submissions`, body,{'headers':headers})
  }

  reviewSubmission(reviewd,date,user_name,time_type,hours): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'user_name':user_name, 
                                'reviewd':reviewd,
                                'date':date,
                                'time_type':time_type,
                                'hours':hours
                            });
    // console.log(body)
    return this.http.post(`${API_URL}/review_time`, body,{'headers':headers})
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

}