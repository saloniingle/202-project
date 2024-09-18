import {Component, CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet} from '@angular/router';
import {NgxSpinnerModule} from "ngx-spinner";
import { NotifierModule } from 'angular-notifier';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ RouterOutlet, RouterLink, RouterLinkActive, NgxSpinnerModule, NotifierModule],
  templateUrl: './app.component.html',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Canvas_clone';
}
