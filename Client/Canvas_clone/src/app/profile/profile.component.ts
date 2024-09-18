import { Component, KeyValueDiffers, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule,FormsModule } from '@angular/forms';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { CommonModule } from '@angular/common';
import {NgxSpinnerModule, NgxSpinnerService} from "ngx-spinner";
import { MatButtonModule } from '@angular/material/button';
import {NotifierModule, NotifierService} from "angular-notifier";
import {ProfileService} from "../services/profile.service";

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatSlideToggleModule,ReactiveFormsModule,FormsModule, CommonModule, MatButtonModule, NgxSpinnerModule, NotifierModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit{
  profileForm: FormGroup;
  private notifier: NotifierService;

  constructor(private fb: FormBuilder, private profileService: ProfileService, private spinner: NgxSpinnerService, private notifierService: NotifierService){
    this.notifier = notifierService;
  }

  ngOnInit(): void {
    this.spinner.show();
    this.profileForm = this.fb.group({
      firstname: ['', Validators.required],
      username: ['', Validators.required],
      lastname: ['', Validators.required],
      isNotificationEnabled: [false, Validators.required]
    })

    this.profileService.get().subscribe(
      {
        next: (data) => {
          var data2 = Object(data);
          this.profileForm.controls["firstname"].setValue(data2["first_name"]);
          this.profileForm.controls["lastname"].setValue(data2["last_name"]);
          this.profileForm.controls["username"].setValue(data2["username"]);
          this.profileForm.controls["isNotificationEnabled"].setValue(data2["notification"])
          },
        error: error => {
          console.log("Error occurred while fetching the profile service");
          this.spinner.hide();
          this.notifier.notify('error', 'There was some issue fetching the profile details');
        },
        complete:()=>{
          this.spinner.hide();
        }
      }
    )
  }

  onSubmit(){
    if(this.profileForm.invalid)
    {
      console.log("Profile form is invalid");
      return;
    }

    this.profileService.put(
      this.profileForm.controls["username"].getRawValue(),
      this.profileForm.controls["isNotificationEnabled"].getRawValue(),
      this.profileForm.controls["firstname"].getRawValue(),
      this.profileForm.controls["lastname"].getRawValue()
    ).subscribe(
      {
        next: (data) => {
          this.spinner.show();
          },
        error: error => {
          this.spinner.hide();
          this.notifier.notify('error', 'There was some issue updating the profile details');
        },
        complete:()=>{
          this.spinner.hide();
        }
      }
    );
  }
}
