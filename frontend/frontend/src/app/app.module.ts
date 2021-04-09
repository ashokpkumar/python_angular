import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HttpClientModule} from '@angular/common/http';
import { FormsModule } from '@angular/forms'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ExamsComponent } from './exams/exams.component';
import { ExamsApiService } from './exams/exams.service';
import { EmployeesComponent } from './employees/employees.component';
import { employeesApiService } from './employees/employees.service';
import { AddEmployeeComponent } from './add-employee/add-employee.component';
import { ViewProjectsComponent } from './projects/view-projects.component';
import { AddProjectsComponent } from './add-projects/add-projects.component';
import { AssignProjectResourceComponent } from './assign-project-resource/assign-project-resource.component';
import { AssignResourceProjectComponent } from './assign-resource-project/assign-resource-project.component';
import { projectsApiService } from './projects/projects.services';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NavigationComponent } from './navigation/navigation.component';
import { HomeComponent } from './home/home.component';
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
   
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    FontAwesomeModule
  ],
  providers: [ExamsApiService,employeesApiService,projectsApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
