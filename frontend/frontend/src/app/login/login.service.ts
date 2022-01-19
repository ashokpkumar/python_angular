import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import {login,setpass} from './login';
import { ToastrService } from 'ngx-toastr';
@Injectable({providedIn:'root'})
export class loginService {
  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  showMessage(message, title){
    console.log("Title : ",title);
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
  addProject(login:login): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(login);
    console.log(body)
    return this.http.post(`${API_URL}/login`, body,{'headers':headers})
  }

  setPassword(login:login):Observable<any>{
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(login);
    console.log(body)
    return this.http.post(`${API_URL}/setpassword`, body,{'headers':headers})
  }
 
}