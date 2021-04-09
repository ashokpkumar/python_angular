import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {EmployeesComponent} from './employees/employees.component';
import {AddEmployeeComponent} from './add-employee/add-employee.component';
import {ViewProjectsComponent} from './projects/view-projects.component';
import {AddProjectsComponent} from './add-projects/add-projects.component';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'employee', component: EmployeesComponent },
  { path: 'addemployee', component: AddEmployeeComponent },
  { path: 'project', component: ViewProjectsComponent },
  { path: 'addproject', component: AddProjectsComponent },
  { path: 'login', component: LoginComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
