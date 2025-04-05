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
import { Subscription } from 'rxjs';
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
        localStorage.setItem('token', response.token);
        //TODO cria page Dashboard
        // this._router.navigate(['/dashboard']);
      },
      (error) => {
        if (error.status === 401) {
          this.errorMessage = 'Usuário ou senha inválidos!';
        } else if (error.status === 500) {
          this.errorMessage = 'Erro no servidor!';
        } else if (error.status === 403) {
          //TODO criar page de erro 403
          // this._router.navigate(['/erro-api']);
        }
      }
    );
    this._subs.add(sub);
  }
}
