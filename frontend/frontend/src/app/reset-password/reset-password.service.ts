import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import {API_URL} from '../env';

@Injectable({
  providedIn: 'root'
})
export class ResetPasswordService {

  constructor(private http: HttpClient) { }

 resetPassword(value): Observable<any> {
    const headers = { 'content-type': 'application/json'};
    const body=JSON.stringify(value);
   
     return this.http.post(`${API_URL}/reset_pass`, body,{'headers':headers})
  }
}
