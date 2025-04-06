import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { StringConstants } from '../../shared/constants/string-constans';

@Component({
  selector: 'app-error-api',
  imports: [],
  templateUrl: './error-api.component.html',
  styleUrl: './error-api.component.scss',
})
export class ErrorApiComponent implements OnInit, OnDestroy {
  title = '';
  text = '';
  button = '';
  statusCode = '';

  private _router = inject(ActivatedRoute);
  private _route = inject(Router);
  private _subs = new Subscription();

  ngOnInit(): void {
    this._controllerError();
  }

  ngOnDestroy(): void {
    this._subs.unsubscribe();
  }

  private _controllerError() {
    const sub = this._router.queryParams.subscribe((params) => {
      const status = params['status'];
      this.statusCode = status;
      switch (status) {
        case '403':
          this.title = StringConstants.ERROR_fORBIDDEN_TITLE;
          this.text = StringConstants.ERROR_fORBIDDEN_TEXT;
          this.button = StringConstants.ERROR_fORBIDDEN_BUTTON;
          break;
        case '404':
          this._route.navigate(['/**'], {});
          break;
        case '500':
          this.title = StringConstants.ERROR_SERVER_TITLE;
          this.text = StringConstants.ERROR_SERVER_TEXT;
          this.button = StringConstants.ERROR_SERVER_BUTTON;
          break;
        default:
          break;
      }
    });
    this._subs.add(sub);
  }
}
