import {employee} from './employees';
import {API_URL} from '../env';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({providedIn:'root'})

export class addEmployeeService{
    constructor(private http: HttpClient) {
    }

    addEmployee(employee:employee):Observable<any>{
        const headers = { 'content-type': 'application/json'}  
        const body=JSON.stringify(employee);
        console.log(body);
        return this.http.post(`${API_URL}/addEmployee`, body,{'headers':headers})
    }
}