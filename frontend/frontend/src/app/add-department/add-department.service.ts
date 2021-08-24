import {API_URL} from '../env';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { department } from './department-info';


@Injectable({providedIn:'root'})

export class addDepartmentService{
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
    addDepartment(department:department):Observable<any>{
        const headers = { 'content-type': 'application/json'}  
        const body=JSON.stringify(department);
        console.log(body);
        return this.http.post(`${API_URL}/addDepartment`, body,{'headers':headers})
    }
}