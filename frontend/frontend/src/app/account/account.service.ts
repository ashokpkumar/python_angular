import {Injectable} from '@angular/core';
 import {HttpClient, HttpErrorResponse} from '@angular/common/http';
 import {Observable, throwError} from 'rxjs';
 import { catchError, map, tap } from 'rxjs/operators';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable()
export class accountApiService {
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

    getEmployeeData(){
        return this.http.get(`${API_URL}/employees`);
    }
}

