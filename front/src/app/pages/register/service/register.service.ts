import { Injectable } from '@angular/core';
import { UserRegister } from '../interfaces/models/user-register';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {

  readonly endpoint = 'http://localhost:5000/user/register';

  constructor(private _httpClient: HttpClient) {}

  makeRegister(nickname: string, password: string): Observable<UserRegister | null> {
    return this._httpClient
      .post<UserRegister | null>(`${this.endpoint}`, JSON.stringify({ name: nickname, pswd: password }))
      .pipe(catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }));
  }
}
