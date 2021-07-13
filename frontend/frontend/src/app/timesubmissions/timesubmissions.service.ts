import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {API_URL} from '../env';
import { ToastrService } from 'ngx-toastr';

@Injectable({providedIn:'root'})
export class timeSubmissionsService {

  constructor(public toastr: ToastrService,private http: HttpClient) {
  }
  
  getSubmissions(user_id): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user_id);
    console.log(body)
    return this.http.post(`${API_URL}/view_submissions`, body,{'headers':headers})
  }

  getTimeData(user_id): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    //const body=JSON.stringify(user_id);
    const body=JSON.stringify({'user_id':user_id});

    console.log(body)
    return this.http.post(`${API_URL}/timeData`, body,{'headers':headers})
  }

  reviewSubmission(reviewd,date,user_name,time_type,hours): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'user_name':user_name, 
                                'reviewd':reviewd,
                                'date':date,
                                'time_type':time_type,
                                'hours':hours 
                            });
 
    return this.http.post(`${API_URL}/review_time`, body,{'headers':headers})
  }

  getSubmissionsBy(user){
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(user);
    console.log(body)
    return this.http.post(`${API_URL}/getSubmissionsBy`, body,{'headers':headers})
  }

  getTimeBy(user,user_name,type){
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'user':user,'user_name':user_name,'type':type});
    console.log('Body : ',body);
    return this.http.post(`${API_URL}/getTimeBy`, body,{'headers':headers})
  }
  getSubmissionByDate(fromDate,toDate){
    console.log(fromDate,toDate)
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify({'fromDate':fromDate,'toDate':toDate});
    console.log('Body : ',body);
    return this.http.post(`${API_URL}/getSubmissionByDate`, body,{'headers':headers})
  }
  rawData(raw_data) {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(raw_data);
    console.log(body)
    return this.http.post(`${API_URL}/rawDataDownload`, body,{'headers':headers})
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
downloadFile(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data, ['user_id','user_name','project_time','bench','SL','CL','AL','total_hrs','Unapproved'
  ]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}
download_timeinfo(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data, ['date_info','user_id','time_type','hours','status' ]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}
download_timeinfoRawData(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data, ["date_info","hours","id","manager_id","project_code","status","submission_id","time_type","user_id"]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}

download_reviewtime(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data, ['date_info','user_id','time_type','hours','status' ]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}
download_reviewtimeRawData(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data, ["date_info","hours","id","manager_id","project_code","status","submission_id","time_type","user_id"]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}
download_rawdata(data, filename='data') {
  console.log(data)
  let csvData = this.ConvertToCSV(data,["date_info","hours","id","manager_id","project_code","status","submission_id","time_type","user_id"]);
  console.log(csvData)
  let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
  let dwldLink = document.createElement("a");
  let url = URL.createObjectURL(blob);
  let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
  if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
  }
  dwldLink.setAttribute("href", url);
  dwldLink.setAttribute("download", filename + ".csv");
  dwldLink.style.visibility = "hidden";
  document.body.appendChild(dwldLink);
  dwldLink.click();
  document.body.removeChild(dwldLink);
}

ConvertToCSV(objArray, headerList) {
  console.log(objArray)
  console.log(typeof(objArray))
   let array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
   console.log(array)
   let str = '';
   let row = 'S.No,';

   for (let index in headerList) {
       row += headerList[index] + ',';

       
   }
   console.log(row)
   row = row.slice(0, -1);

   str += row + '\r\n';
   console.log(row)
   console.log(array.length)
   for (let i = 0; i < array.length; i++) {
       let line = (i+1)+'';
       for (let index in headerList) {
         console.log(index)
          let head = headerList[index];
            console.log(array)
            console.log(head)
            console.log(i)
            console.log(array[i])
            console.log(array[i][head.toLowerCase()])

           line += ',' + array[i][head.toLowerCase()];
       }
       console.log(line)
       str += line + '\r\n';
   }
   console.log(str)
   return str;
}

}