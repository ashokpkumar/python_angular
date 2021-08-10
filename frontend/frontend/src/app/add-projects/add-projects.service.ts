import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {project} from './projects';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class addProjectApiService {
 
  baseURL: string = "http://localhost:3000/";
 
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
  addProject(project:project): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(project);
   
    return this.http.post(`${API_URL}/addProject`, body,{'headers':headers})
  }
 
}