import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'register',
    loadComponent: () =>
      import('./pages/register/register.component').then(c => c.RegisterComponent),
  },
  {
    path: '',
    loadComponent: () =>
      import('./pages/login/login.component').then(c => c.LoginComponent),
  },
];
