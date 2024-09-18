import { Component ,Inject} from '@angular/core';
import { MatDialogRef ,MAT_DIALOG_DATA,MatDialogModule,MatDialogActions} from '@angular/material/dialog';
import { CourseService} from '../services/course.service';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators,FormsModule,ReactiveFormsModule} from '@angular/forms';
import {MatButton} from '@angular/material/button';
import { AssignmentsService } from '../services/assignments.service';
import { MatFormFieldModule} from "@angular/material/form-field";
export interface DialogData {
  courseId: string;
} 

@Component({
  selector: 'app-add-assignment',
  standalone: true,
  imports: [MatDialogActions,MatDialogModule,MatDialogModule,MatButton,FormsModule,ReactiveFormsModule,MatFormFieldModule],  
  templateUrl: './add-assignment.component.html',
  styleUrl: './add-assignment.component.css'
})
export class AddAssignmentComponent {
  constructor(private ref:MatDialogRef<AddAssignmentComponent>,@Inject(MAT_DIALOG_DATA) public data: DialogData,private courseService:CourseService,public router:Router,private assignmentService:AssignmentsService){}
  assignmentForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    grade: new FormControl('', [Validators.required]),
  });
  
  
  closeModal(){
    this.ref.close();
  }
  onsubmit() {
    if (this.assignmentForm.invalid) {
      return;
    }
    if (this.assignmentForm.value.description && this.assignmentForm.value.title && this.assignmentForm.value.grade) {
    this.assignmentService.create(Number(this.data.courseId),{
      title:this.assignmentForm.value.title,
      description:this.assignmentForm.value.description,
      maxGrade:this.assignmentForm.value.grade
    })
      .subscribe({
        next:(result)=>{
          console.log(result);
          this.ref.close();
        },
        error: (err:any) => {
          console.log(err)
        },
        complete: () => {
        }})
      }
    }
}
