import {Injectable} from '@angular/core';
 import {HttpClient, HttpErrorResponse} from '@angular/common/http';
 import {Observable, throwError} from 'rxjs';
 import { catchError, map, tap } from 'rxjs/operators';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';
import {projectResource} from './assign';
import {projectManager} from './assignPM';
import { ResourceList } from './Resourcelist';

@Injectable()
export class projectsApiService {
    public employeesList: any;
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
  getProjects() {
    return this.http.get(`${API_URL}/projects`);
}
getEmployees() {
  return this.http.get(`${API_URL}/employees`);
}

getResourceInfo(ResourceList:ResourceList):Observable<any>{
console.log(ResourceList)
const headers = { 'content-type': 'application/json'}  
const body=JSON.stringify(ResourceList);
console.log(body);
return this.http.post(`${API_URL}/getResourceInfo`, body,{'headers':headers})
}

addProjectResource(projectResource:projectResource): Observable<any> {
  const headers = { 'content-type': 'application/json'}  
  const body=JSON.stringify(projectResource);
  console.log(body);
  return this.http.post(`${API_URL}/addProjectResource`, body,{'headers':headers})
}

removeProjectResource(emp_id,project_id){
  const headers = { 'content-type': 'application/json'}  
  const body=JSON.stringify({'emp_id':emp_id,'project_id':project_id});
  console.log(body);
  return this.http.post(`${API_URL}/removeProjectResource`, body,{'headers':headers})
}

addProjectManager(projectManager:projectManager): Observable<any> {
  const headers = { 'content-type': 'application/json'}  
  const body=JSON.stringify(projectManager);
  console.log(body);
  return this.http.post(`${API_URL}/addProjectmanager`, body,{'headers':headers})
}

}