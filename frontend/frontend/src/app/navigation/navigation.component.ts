import { Component, OnInit,HostListener } from '@angular/core';
import { faSearch, faBell, faUser, faHome , faMapMarkerAlt,faPhoneAlt,faPowerOff} from '@fortawesome/free-solid-svg-icons';
import {CookieService} from 'ngx-cookie-service';
import { ToastrService } from 'ngx-toastr';
import {Router} from "@angular/router";
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
  faHome = faHome;
  faPhoneAlt = faPhoneAlt;
  faMapMarkerAlt = faMapMarkerAlt;
  faPowerOff = faPowerOff;

  constructor(private router: Router,public toastr: ToastrService,private cookieService: CookieService) { }

  public ngOnInit(): void {
    this.cookieService.set('cookie-name','our cookie value');
    this.cookieValue = this.cookieService.get('cookie-name');
    console.log("Cookie value", this.cookieValue);
  }
  logout(){
    console.log("Logging out ")
    this.cookieService.set('login','false');
    
    this.router.navigate(['/login']);
  }
  menuHover(className){
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
  }
document.getElementById(className).classList.toggle("show");

}
menuLeave(className){
  document.getElementById(className).classList.remove("show");
  }
@HostListener('document:click', ['$event'])
onDocumentClick(event: MouseEvent) {
  var ele=<Element>event.target;
  if (!ele.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

}
