import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import {login} from './login';

@Injectable({providedIn:'root'})
export class loginService {
  constructor(private http: HttpClient) {
  }
  
  addProject(login:login): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(login);
    console.log(body)
    return this.http.post(`${API_URL}/login`, body,{'headers':headers})
  }
 
}