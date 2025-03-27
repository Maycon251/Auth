import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { RegisterService } from './service/register.service';

@Component({
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  registerForm!: FormGroup;
  messageSuccess = '';
  messageError = '';

  private _formBuilder = inject(FormBuilder);
  private _router = inject(Router);
  private _registerService = inject(RegisterService);

  constructor() {
    this.registerForm = this._formBuilder.group({
      nickname: ['', [Validators.required, Validators.pattern(/^[^\d]*$/)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit() {
    if (this.registerForm.valid) {
      this._registerService
        .makeRegister(this.registerForm.value.nickname, this.registerForm.value.password)
        .subscribe((response) => {
          if (response) {
            window.location.href = '/';
          }
        }, (error) => {
          this.messageError = 'Usuário já cadastrado!';
        });
    }
  }
}
