import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SpinnerService {
  public spinnerVisibility = new BehaviorSubject<boolean>(false);

  show() {
    this.spinnerVisibility.next(true);
  }

  hide() {
    this.spinnerVisibility.next(false);
  }

  getSpinnerVisibility() {
    return this.spinnerVisibility.asObservable();
  }
}
