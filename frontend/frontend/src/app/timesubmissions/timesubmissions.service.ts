import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class timeSubmissionsService {

  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  
  getSubmissions(user_id): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user_id);
    console.log(body)
    return this.http.post(`${API_URL}/view_submissions`, body,{'headers':headers})
  }

  getTimeData(user_id): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user_id);
    console.log(body)
    return this.http.post(`${API_URL}/timeData`, body,{'headers':headers})
  }

  reviewSubmission(reviewd,date,user_name,time_type,hours): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'user_name':user_name, 
                                'reviewd':reviewd,
                                'date':date,
                                'time_type':time_type,
                                'hours':hours 
                            });
 
    return this.http.post(`${API_URL}/review_time`, body,{'headers':headers})
  }

  getSubmissionsBy(user ){
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user);
    console.log(body)
    return this.http.post(`${API_URL}/getSubmissionsBy`, body,{'headers':headers})
  }

  getTimeBy(user,user_name,type){
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'user':user,'user_name':user_name,'type':type});
    console.log('Body : ',body);
    return this.http.post(`${API_URL}/getTimeBy`, body,{'headers':headers})
  }
  getSubmissionByDate(fromDate,toDate){
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'fromDate':fromDate,'toDate':toDate});
    console.log('Body : ',body);
    return this.http.post(`${API_URL}/getSubmissionByDate`, body,{'headers':headers})
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