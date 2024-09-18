import {Component, Inject, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {DOCUMENT, NgForOf, NgIf} from "@angular/common";
import { QuizzesService,StudentsGrade,QuizInfo } from '../services/quizzes.service';
import {MatButton, MatButtonModule} from "@angular/material/button";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {
  MAT_DIALOG_DATA, MatDialog,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {NotifierModule, NotifierService} from "angular-notifier";
export interface DialogData {
  courseID: number;
  quizID:number;
  enrollment_id:number;
  studentName:string;
  maxGrade:number
}

@Component({
  selector: 'app-quiz',
  standalone: true,
  imports: [MatButton,NgForOf,NgIf, NotifierModule],
  templateUrl: './quiz.component.html',
  styleUrl: './quiz.component.css'
})

export class QuizComponent implements OnInit {
  courseID:any;
  quizID: any
  userType:string|null;
  students: StudentsGrade[] = [];
  quiz:QuizInfo;
  student: {
  "quizId": number,
  "enrollmentId": number,
  "grade": number,
  "gradeId": number,
  "maxGrade": number
   }

  private readonly notifier: NotifierService;

  constructor(@Inject(DOCUMENT) private document: Document, private route: ActivatedRoute,
              private quizService: QuizzesService,  public dialog: MatDialog, notifierService: NotifierService) {
    const localStorage = document.defaultView?.localStorage;
    this.notifier = notifierService;

    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }
  }

  ngOnInit(): void {
    this.courseID = this.route.snapshot.paramMap.get('courseID');
    this.quizID = this.route.snapshot.paramMap.get('quizID');
    if(this.userType=="student"){
      this.loadQuizByIdForStudent();
    }
    else{
    this.loadQuizById();
    }
  };

loadQuizById(){
  this.quizService.get(this.courseID,this.quizID).subscribe({
    next: (result: any) => {
      this.quiz = result.quizInfo;
      this.students = result.studentGrades;
    },
    error: (err) => {
      console.log(err)
    }
  })
}
loadQuizByIdForStudent() {
  this.quizService.getForStudent(this.courseID, this.quizID)
    .subscribe({
      next: (result) => {
        this.quiz = result.quizInfo;
        this.student = result.studentGrades;
      },
      error: (err) => {
        console.log(err)
      }
    })
}
  openDialog(studentName:string, enrollment_id:number, maxGrade:number): void {
    const dialogRef = this.dialog.open(AssignGradeModal, {
      height: '200px',
      width: '600px',
      data: {courseID: this.courseID, quizID:this.quizID, enrollment_id:enrollment_id, studentName:studentName,  maxGrade:maxGrade}
    });

    dialogRef.afterClosed().subscribe(error => {
      this.loadQuizById();
      console.log(error)
      if(error==false) this.notifier.notify('success', 'Grade assigned');
      if (error==true) this.notifier.notify('error', 'Error assigning grade');

    });
  }

}

@Component({
  selector: 'assign-grade-modal',
  templateUrl: '../modals/assign-grade-modal.html',
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
export class AssignGradeModal {
  constructor(
    public dialogRef: MatDialogRef<AssignGradeModal>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,private  quizservice: QuizzesService
  ) {}

  assignGradeForm = new FormGroup({
    grade: new FormControl(0, [Validators.required]),
  });

  onNoClick(): void {
    this.dialogRef.close();
  }

  gradeAssigned:boolean = false;
  studentName = this.data.studentName
  maxGrade= this.data.maxGrade;

  onsubmit() {
    if (this.assignGradeForm.invalid || this.assignGradeForm.value==null || this.assignGradeForm.value.grade==null) {
      return;
    }
    if (this.assignGradeForm.value.grade >= -1) {
      this.quizservice.assignGrade(Number(this.data.courseID),Number(this.data.quizID), {
        student_grades: this.assignGradeForm.value.grade,
        enrollment_id:Number(this.data.enrollment_id)
      }).subscribe({
        next: (result) => {
          this.gradeAssigned = true
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
