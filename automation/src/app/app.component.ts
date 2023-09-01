import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'automation';
  constructor(private router: Router){}
  OnNavigate(){
    this.router.navigate(['form']); // Replace '/target-route' with the route you want to navigate to
  }
}
