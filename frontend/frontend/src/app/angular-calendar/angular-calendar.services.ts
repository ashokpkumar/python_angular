import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class AngularCalendarService {
  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  getEvents(): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body="";
    console.log(body)
    return this.http.post(`${API_URL}/getsampleevents`, body,{'headers':headers})
  }
  
}