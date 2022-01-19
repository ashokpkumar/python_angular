import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {projectResource} from './assign';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class addProjectResourceApiService {
 // 
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
onSubmit(projectResource:projectResource): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(projectResource);
    console.log(body)
    return this.http.post(`${API_URL}/addProjectResource`, body,{'headers':headers})
  }
 
}