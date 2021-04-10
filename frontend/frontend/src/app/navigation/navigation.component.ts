import { Component, OnInit } from '@angular/core';
import { faSearch, faBell, faUser } from '@fortawesome/free-solid-svg-icons';
import {CookieService} from 'ngx-cookie-service';
import { ToastrService } from 'ngx-toastr';
@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {
  
  private cookieValue: string;
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
  faSearch = faSearch;
  faBell = faBell;
  faUser = faUser;
  constructor(public toastr: ToastrService,private cookieService: CookieService) { }

  public ngOnInit(): void {
    this.cookieService.set('cookie-name','our cookie value');
    this.cookieValue = this.cookieService.get('cookie-name');
    console.log("Cookie value", this.cookieValue);
  }

}
