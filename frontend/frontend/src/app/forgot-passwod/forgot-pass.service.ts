import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';

@Injectable({
  providedIn: 'root'
})
export class ForgotPassService {

  constructor(private http: HttpClient) { }
  forgetPass(value): Observable<any> {
    const headers = { 'content-type': 'application/json'};

    const body=JSON.stringify({email_id:value});
    console.log(value);
     return this.http.post(`${API_URL}/forgot_pass_create_token`, body,{'headers':headers})
  }
}
