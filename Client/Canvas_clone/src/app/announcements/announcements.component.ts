import {Component, Inject, OnInit} from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {NgxSpinnerModule, NgxSpinnerService} from "ngx-spinner";
import {NotifierModule, NotifierService} from "angular-notifier";
import {DOCUMENT, NgForOf, NgIf} from "@angular/common";
import {Course, CourseService} from "../services/course.service";
import {ActivatedRoute, Route, Router} from "@angular/router";
import {AuthenticationService} from "../services/authentication.service";
import {Announcement, AnnouncementsService} from "../services/announcements.service";
import {MatCard, MatCardHeader, MatCardTitle} from "@angular/material/card";
import {MatButton, MatButtonModule} from "@angular/material/button";
import {
  MAT_DIALOG_DATA,
  MatDialog, MatDialogActions, MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatFormField, MatFormFieldModule, MatLabel} from "@angular/material/form-field";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatInput, MatInputModule} from "@angular/material/input";

export interface DialogData {
  courseID: string;
}

@Component({
  selector: 'app-announcements',
  standalone: true,
  imports: [
    MatToolbar,
    NgxSpinnerModule,
    NotifierModule,
    NgIf,
    MatCard,
    MatCardHeader,
    MatCardTitle,
    NgForOf,
    MatButton,
  ],
  templateUrl: './announcements.component.html',
  styleUrl: './announcements.component.css'
})
export class AnnouncementsComponent implements OnInit{
  userType:string|null;
  userID:number;
  courseID:string | null;
  course:Course;
  announcements:Announcement[]
  private readonly notifier: NotifierService;
  constructor(@Inject(DOCUMENT) private document: Document, private coursesService: CourseService, notifierService: NotifierService, private router:ActivatedRoute,
              private spinner: NgxSpinnerService, protected authenticationService:AuthenticationService,
              private  announcementsService: AnnouncementsService, public dialog: MatDialog
  ) {
    const localStorage = document.defaultView?.localStorage;

    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }
    if(localStorage?.getItem('user_id')){
      this.userID = Number(localStorage.getItem('user_id'))
    }
    this.notifier = notifierService;
    this.router.paramMap.subscribe( paramMap => {
      this.courseID = paramMap.get('courseID');
    })
  }

  openDialog() {
    const dialogRef = this.dialog.open(CreateAnnouncementModal, {data:{
      courseID:this.courseID},
      height: '400px',
      width: '700px'
    });

    dialogRef.afterClosed().subscribe(result => {
      this.getAllAnnouncements();
    });

  }
  ngOnInit() {
    if (this.courseID != null) {
      this.coursesService.getById(Number(this.courseID)).subscribe({
        next: (result) => {
          this.course = result;
        },
        error: (err) => {
          console.log(err)
        },
        complete: () => {
          this.spinner.hide();
        }
      })
    }
    this.getAllAnnouncements();
  }

  getAllAnnouncements(){
    this.announcementsService.getAll(Number(this.courseID)).subscribe({
      next: (result) => {
        this.announcements = result;
      },
      error: (err) => {
        console.log(err)
      },
      complete: () => {
        this.spinner.hide();
      }
    })
  }
}


@Component({
  selector: 'announcement-modal',
  templateUrl: '../modals/announcement-modal.html',
  standalone: true,
  imports: [MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose, ReactiveFormsModule],
})
export class CreateAnnouncementModal {
  constructor(
    public dialogRef: MatDialogRef<CreateAnnouncementModal>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,private  announcementsService: AnnouncementsService
  ) {}
  announcementForm = new FormGroup({
    body: new FormControl('', [Validators.required]),
  });
  onNoClick(): void {

    this.dialogRef.close();
  }

  onsubmit() {
    if (this.announcementForm.invalid) {
      return;
    }
    if (this.announcementForm.value.body) {
      this.announcementsService.create(Number(this.data.courseID), {
        announcementText: this.announcementForm.value.body
      }).subscribe({
        next: (result) => {
          console.log(result);
        },
        error: (err) => {
          console.log(err)
        },
        complete: () => {
        }
      })
    }
  }
}
