import { CommonModule } from '@angular/common';
import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { RegisterService } from './service/register.service';
import { Subscription } from 'rxjs';

@Component({
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent implements OnDestroy {
  registerForm!: FormGroup;
  messageSuccess = '';
  messageError = '';
  private _subs = new Subscription();

  private _formBuilder = inject(FormBuilder);
  private _router = inject(Router);
  private _registerService = inject(RegisterService);

  constructor() {
    this.registerForm = this._formBuilder.group({
      nickname: ['', [Validators.required, Validators.pattern(/^[^\d]*$/)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  ngOnDestroy(): void {
    this._subs.unsubscribe();
  }

  onSubmit() {
    if (this.registerForm.valid) {
      const sub = this._registerService
      .makeRegister(this.registerForm.value)
      .subscribe((response) => {
        if (response) {
          this._router.navigate(['/']);
        } 
      }, (error) => {
        if (error.status === 401) {
          this.messageError = 'Usuário já cadastrado!';
        } else if (error.status === 500) {
          this.messageError = 'Erro no servidor!';
        }
      });
      this._subs.add(sub);
    }
    
  }
}
