import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {project} from './projects';
import {API_URL} from '../env';

@Injectable({providedIn:'root'})
export class addProjectApiService {
 
  baseURL: string = "http://localhost:3000/";
 
  constructor(private http: HttpClient) {
  }
  
  addProject(project:project): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(project);
    console.log(body)
    return this.http.post(`${API_URL}/addProject`, body,{'headers':headers})
  }
 
}