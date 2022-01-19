import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
 import {userInfo} from './time';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class showTimeApiService {
 // 
  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  
  onSubmit(userInfo:userInfo): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(userInfo);
    console.log(body)
    return this.http.post(`${API_URL}/viewEmpInfo`, body,{'headers':headers})
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