import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UserLogin } from '../interfaces/models/user-login';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  readonly endpoint = '/user/login';

  constructor(private _httpClient: HttpClient) {}

  loginUser(user: UserLogin): Observable<{ acess_token: string }> {
    return this._httpClient.post<{ acess_token: string }>(
      `${this.endpoint}`,
      user,
      {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true,
      }
    );
  }
}
