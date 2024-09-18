import { Component } from '@angular/core';
import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators,
  FormsModule,
  ReactiveFormsModule, FormGroup,
} from '@angular/forms';
import {ErrorStateMatcher} from '@angular/material/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from "@angular/material/icon";
import {MatDividerModule} from "@angular/material/divider";
import {MatButtonModule} from "@angular/material/button";
import {AuthenticationService} from "../services/authentication.service";
import {HttpClientModule} from "@angular/common/http";
import {NgxSpinnerModule, NgxSpinnerService} from "ngx-spinner";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {Router} from "@angular/router";
import {NotifierModule, NotifierService} from "angular-notifier";

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MatFormFieldModule, MatInputModule, ReactiveFormsModule, MatButtonModule, MatDividerModule, MatIconModule, HttpClientModule, NgxSpinnerModule, NotifierModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})


export class LoginComponent {
  constructor(
    private authenticationService:AuthenticationService,
    private spinner: NgxSpinnerService,
    private router: Router,
    notifierService: NotifierService
  ) {
    this.notifier = notifierService;
  }

  private readonly notifier: NotifierService;

  matcher = new MyErrorStateMatcher();

  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
  });


  onsubmit(){
    if (this.loginForm.invalid) {
          return;
        }
    if(this.loginForm.value.username  && this.loginForm.value.password){
      this.spinner.show();
      this.authenticationService.login(this.loginForm.value.username, this.loginForm.value.password).subscribe(
        {
          next: (data) => {
            this.spinner.hide();
            this.router.navigateByUrl('courses');
          },
          error: error => {
            this.spinner.hide();
            this.notifier.notify('error', 'Issue logging in, please check username and password');
          }
        }
      )
    }
  }
}
