import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'register',
    loadComponent: () =>
      import('./pages/register/register.component').then(
        (c) => c.RegisterComponent
      ),
    title: 'Sistema de automação - Registro',
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component').then((c) => c.LoginComponent),
    title: 'Sistema de automação - Login',
  },
  {
    path: '',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component').then(
        (c) => c.DashboardComponent
      ),
    title: 'Sistema de automação - Dashboard',
  },
  {
    path: '**',
    loadComponent: () =>
      import('./pages/not-found/not-found.component').then(
        (c) => c.NotFoundComponent
      ),
    title: 'Página não encontrada',
  },
];
