import {Component, Inject, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {DOCUMENT, NgForOf, NgIf} from "@angular/common";
import {AssignmentInfo, AssignmentsService, StudentsGrade} from "../services/assignments.service";
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
  assignmentID:number;
  enrollment_id:number;
  studentName:string;
  maxGrade:number;
}


@Component({
  selector: 'app-assignment',
  standalone: true,
  imports: [
    MatButton,
    NgForOf,
    NgIf,
    NotifierModule,
  ],
  templateUrl: './assignment.component.html',
  styleUrl: './assignment.component.css'
})
export class AssignmentComponent implements OnInit{
  courseID:any;
  assignmentID: any
  userType:string|null;
  students: StudentsGrade[] = [];
  assignment:AssignmentInfo;
  student: {
  "assignmentId": number,
  "enrollmentId": number,
  "grade": number,
  "gradeId": number,
  "maxGrade": number
   }

  private readonly notifier: NotifierService;

  constructor(@Inject(DOCUMENT) private document: Document, private route: ActivatedRoute,
              private assignmentService: AssignmentsService,  public dialog: MatDialog, notifierService: NotifierService) {
    const localStorage = document.defaultView?.localStorage;
    this.notifier = notifierService;
    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      if(params.get('courseID')){
        this.courseID = params.get('courseID')
      }
      if(params.get('assignmentID')){
        this.assignmentID = params.get('assignmentID')
      }
      if(this.userType=="student"){
        this.loadAssignmentByIdForStudent();
      }
      else{
      this.loadAssignmentById();
      }
    });
  }

  loadAssignmentById() {
    this.assignmentService.get(this.courseID, this.assignmentID)
      .subscribe({
        next: (result) => {
          this.assignment = result.assignmetInfo;
          this.students = result.studentGrades;
        },
        error: (err) => {
          console.log(err)
        }
      })
  }

  loadAssignmentByIdForStudent() {
    this.assignmentService.getForStudent(this.courseID, this.assignmentID)
      .subscribe({
        next: (result) => {
          this.assignment = result.assignmetInfo;
          this.student = result.studentGrades;
        },
        error: (err) => {
          console.log(err)
        }
      })
  }
  openDialog( studentName:string, enrollment_id:number, maxGrade:number) {
    const dialogRef = this.dialog.open(AssignGradeModal, {data:{
        courseID:this.courseID, assignmentID:this.assignmentID, enrollment_id:enrollment_id, studentName:studentName, maxGrade:maxGrade
      },
      height: '200px',
      width: '600px'
    });

    dialogRef.afterClosed().subscribe(error => {
      this.loadAssignmentById();
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
    @Inject(MAT_DIALOG_DATA) public data: DialogData,private  assignmentService: AssignmentsService,
  ) {
  }
  gradeAssigned:boolean = false;
  studentName = this.data.studentName
  maxGrade:number = this.data.maxGrade;

  assignGradeForm = new FormGroup({
    grade: new FormControl(0, [Validators.required, Validators.pattern(/^[0-9]*$/)]),
  });

  onNoClick(): void {
    this.dialogRef.close();
  }

  onsubmit() {
    if (this.assignGradeForm.invalid || this.assignGradeForm.value==null || this.assignGradeForm.value.grade==null ) {
      return;
    }
    if (this.assignGradeForm.value.grade >=-1 ) {
      this.assignmentService.assignGrade(Number(this.data.courseID),Number(this.data.assignmentID), {
        student_grades: this.assignGradeForm.value.grade,
        enrollment_id:Number(this.data.enrollment_id)
      }).subscribe({
        next: (result) => {
          this.gradeAssigned = true
          console.log(result);
        },
        error: (err) => {
          this.gradeAssigned = false
          console.log(err)
        },
        complete: () => {
        }
      })
    }
  }
}

