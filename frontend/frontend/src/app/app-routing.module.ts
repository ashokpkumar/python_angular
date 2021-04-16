import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {EmployeesComponent} from './employees/employees.component';
import {AddEmployeeComponent} from './add-employee/add-employee.component';
import {ViewProjectsComponent} from './projects/view-projects.component';
import {AddProjectsComponent} from './add-projects/add-projects.component';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';
import {AssignResourceProjectComponent} from './assign-resource-project/assign-resource-project.component';
import {ShowTimeComponent} from './show-time/show-time.component';
import {AccountSummaryComponent} from './account-summary/account-summary.component';
import {PersonalSummaryComponent} from './personal-summary/personal-summary.component';
import {ProfessionalSummaryComponent} from './professional-summary/professional-summary.component';
import {TimeSummaryComponent} from './time-summary/time-summary.component';
import {TimesubmissionsComponent} from './timesubmissions/timesubmissions.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'employee', component: EmployeesComponent },
  { path: 'addemployee', component: AddEmployeeComponent },
  { path: 'project', component: ViewProjectsComponent },
  { path: 'addproject', component: AddProjectsComponent },
  { path: 'login', component: LoginComponent },
  { path: 'addresourceproject', component: AssignResourceProjectComponent },
  { path: 'time', component: TimeSummaryComponent },
  { path: 'professional', component: ProfessionalSummaryComponent },
  { path: 'personal', component: PersonalSummaryComponent },
  { path: 'account', component: AccountSummaryComponent },
  { path: 'timesubmission', component: TimesubmissionsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
