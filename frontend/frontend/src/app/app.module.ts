import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import { FormsModule } from '@angular/forms'
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ReactiveFormsModule } from '@angular/forms';
import {CookieService} from 'ngx-cookie-service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ExamsComponent } from './exams/exams.component';
import { ExamsApiService } from './exams/exams.service';
import { EmployeesComponent } from './employees/employees.component';
import { employeesApiService } from './employees/employees.service';
import { AddEmployeeComponent } from './add-employee/add-employee.component';
import { AddDepartmentComponent } from './add-department/add-department.component';
import { ViewProjectsComponent } from './projects/view-projects.component';
import { AddProjectsComponent } from './add-projects/add-projects.component';
import { AssignProjectResourceComponent } from './assign-project-resource/assign-project-resource.component';
import { AssignResourceProjectComponent } from './assign-resource-project/assign-resource-project.component';
import { projectsApiService } from './projects/projects.services';
import { NavigationComponent } from './navigation/navigation.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import {loginService} from './login/login.service'
import {MatSelectModule} from '@angular/material/select';
import { ShowTimeComponent } from './show-time/show-time.component';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { FullCalendarModule } from '@fullcalendar/angular'; 
import dayGridPlugin from '@fullcalendar/daygrid'; 
import interactionPlugin from '@fullcalendar/interaction'; 
import { MatNativeDateModule } from '@angular/material/core';

import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { PersonalSummaryComponent } from './personal-summary/personal-summary.component';
import { ProfessionalSummaryComponent } from './professional-summary/professional-summary.component';
import { TimeSummaryComponent } from './time-summary/time-summary.component';
import { AccountSummaryComponent } from './account-summary/account-summary.component';
import { TimesubmissionsComponent } from './timesubmissions/timesubmissions.component';
import { IndividualTimeComponent } from './individual-time/individual-time.component';
import { SideBarComponent } from './side-bar/side-bar.component';
import {MatInputModule} from '@angular/material/input'
import {PopoverModule} from "ngx-smart-popover";
import {NgbPopoverModule} from '@ng-bootstrap/ng-bootstrap';
import {Ng2OrderModule } from "ng2-order-pipe";
import {Ng2SearchPipeModule } from "ng2-search-filter";
import { ForgotPasswodComponent } from './forgot-passwod/forgot-passwod.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component'
import {MatTabsModule} from '@angular/material/tabs';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { AddDesignationComponent } from './add-designation/add-designation.component';
import { SortDirective } from './directive/sort.directive';
//import { TokenInterceptor } from './auth/token.interceptor';

FullCalendarModule.registerPlugins([ 
  dayGridPlugin,
  interactionPlugin
]);

@NgModule({
  declarations: [
    AppComponent,
    ExamsComponent,
    EmployeesComponent,
    AddEmployeeComponent,
    ViewProjectsComponent,
    AddProjectsComponent,
    AssignProjectResourceComponent,
    AssignResourceProjectComponent,
    NavigationComponent,
    HomeComponent,
    LoginComponent,
    ShowTimeComponent,
    PersonalSummaryComponent,
    ProfessionalSummaryComponent,
    TimeSummaryComponent,
    AccountSummaryComponent,
    TimesubmissionsComponent,
    IndividualTimeComponent,
    SideBarComponent,
    ForgotPasswodComponent,
    ResetPasswordComponent,
    AddDepartmentComponent,
    AddDesignationComponent,
    SortDirective
   
  ],

  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    FontAwesomeModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    MatSelectModule,
    FullCalendarModule ,
    MatDatepickerModule,
    MatButtonModule,
    MatFormFieldModule,
    MatNativeDateModule, 
    MatDatepickerModule,
    MatButtonModule,
    NgbPopoverModule,
    Ng2OrderModule,
    Ng2SearchPipeModule,
    MatFormFieldModule,
    MatNativeDateModule,
    MatInputModule,
    PopoverModule,
    MatTabsModule,
    CalendarModule.forRoot({
      provide: DateAdapter,
      useFactory: adapterFactory,
    })
  ],
  
  providers: [ExamsApiService,employeesApiService,projectsApiService,loginService,MatDatepickerModule,],
  bootstrap: [AppComponent]
})
export class AppModule { }
