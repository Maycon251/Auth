import { Component, inject, OnInit } from '@angular/core';
import { LoginService } from './service/login.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
  errorMessage: string = '';
  registerForm!: FormGroup;

  private _loginService = inject(LoginService);
  private _formBuilder = inject(FormBuilder);
  private _router = inject(Router);

  ngOnInit(): void {
    this.registerForm = this._formBuilder.group({
      nickname: [''],
      password: [''],
    });
  }

  login() {
    const user = this.registerForm.value;
    this._loginService.loginUser(user).subscribe(
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
  }
}
