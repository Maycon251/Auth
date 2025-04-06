import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { LoginService } from './service/login.service';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { Subscription, throwError } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit, OnDestroy {
  errorMessage: string = '';
  registerForm!: FormGroup;
  messageSuccess = '';
  messageError = '';
  private _subs = new Subscription();

  private _loginService = inject(LoginService);
  private _formBuilder = inject(FormBuilder);
  private _router = inject(Router);

  ngOnInit(): void {
    this.registerForm = this._formBuilder.group({
      nickname: ['', [Validators.required, Validators.pattern(/^[^\d]*$/)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }
  ngOnDestroy(): void {
    this._subs.unsubscribe();
  }

  login() {
    const user = this.registerForm.value;
    const sub = this._loginService.loginUser(user).subscribe(
      (response) => {
        document.cookie = `token=${response.acess_token}; path=/; secure; SameSite=Strict`;
        this._router.navigate(['/']);
      },
      (error) => {
        if (error.status === 401) {
          this.errorMessage = 'Usuário ou senha inválidos!';
        } else if (error.status === 500) {
          this._router.navigate(['/error-api'], {
            queryParams: { status: 500 },
          });
        } else if (error.status === 403) {
          this._router.navigate(['/error-api'], {
            queryParams: { status: 403 },
          });
          return throwError(() => new Error('Acesso negado!'));
        }
        return throwError(() => error);
      }
    );
    this._subs.add(sub);
  }
}
