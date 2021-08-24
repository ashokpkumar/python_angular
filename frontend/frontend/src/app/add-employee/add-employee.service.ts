import {employee} from './employees';
import {API_URL} from '../env';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})

export class addEmployeeService{
    constructor(public toastr: ToastrService, private http: HttpClient) {
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
    
    addEmployee(employee:employee):Observable<any>{
        const headers = { 'content-type': 'application/json'}  
        const body=JSON.stringify(employee);
        console.log(body);
        return this.http.post(`${API_URL}/addEmployee`, body,{'headers':headers})
    }
    getprojectid(){
        return this.http.get(`${API_URL}/getprojectid`);
    }
    getdepartment(){
        return this.http.get(`${API_URL}/getdepartment`);
    }
    getdesignation(){
        return this.http.get(`${API_URL}/getdesignation`);
    }
}