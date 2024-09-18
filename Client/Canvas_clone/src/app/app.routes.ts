import { Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {AuthGuard} from "./guards/auth.guard";

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '',  loadChildren: () => import('../app/home/home.module').then(m => m.HomeModule),  canActivate: [AuthGuard]}
];
