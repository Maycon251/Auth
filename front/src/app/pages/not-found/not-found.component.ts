import { Router } from '@angular/router';
import { StringConstants } from './../../shared/constants/string-constans';
import { Component, inject } from '@angular/core';

@Component({
  selector: 'app-not-found',
  imports: [],
  templateUrl: './not-found.component.html',
  styleUrl: './not-found.component.scss',
})
export class NotFoundComponent {
  title = StringConstants.PAGE_NOT_FOUND_TITLE;
  text = StringConstants.PAGE_NOT_FOUND_TEXT;
  button = StringConstants.PAGE_NOT_FOUND_BUTTON;

  private _router = inject(Router);

  gotoHome() {
    this._router.navigate(['/']);
  }
}
