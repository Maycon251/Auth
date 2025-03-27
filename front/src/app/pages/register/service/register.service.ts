import { Injectable } from '@angular/core';
import { UserRegister } from '../interfaces/models/user-register';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {

  readonly endpoint = '/user/register';

  constructor(private _httpClient: HttpClient) {}

  makeRegister(user: UserRegister): Observable<UserRegister | null> {
    return this._httpClient
      .post<UserRegister | null>(`${this.endpoint}`, JSON.stringify(user))
      .pipe(catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }));
  }
}
