import {Injectable} from '@angular/core';
 import {HttpClient, HttpErrorResponse} from '@angular/common/http';
 import {Observable, throwError} from 'rxjs';
 import { catchError, map, tap } from 'rxjs/operators';
import {API_URL} from '../env';

@Injectable()
export class employeesApiService {
    public employeesList: any;
  constructor(private http: HttpClient) {
  }
  getExams() {
    return this.http.get(`${API_URL}/employees`);
}

}