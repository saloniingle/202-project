import { Component ,Inject} from '@angular/core';
import { MatDialogRef ,MAT_DIALOG_DATA,MatDialogModule,MatDialogActions} from '@angular/material/dialog';
import { CourseService} from '../services/course.service';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators,FormsModule,ReactiveFormsModule} from '@angular/forms';
import {MatButton} from '@angular/material/button';
import { QuizzesService } from '../services/quizzes.service';
import { MatFormFieldModule} from "@angular/material/form-field";
export interface DialogData {
  courseId: string;
} 

@Component({
  selector: 'app-add-quiz',
  standalone: true,
  imports: [MatDialogActions,MatDialogModule,MatDialogModule,MatButton,FormsModule,ReactiveFormsModule,MatFormFieldModule],
  templateUrl: './add-quiz.component.html',
  styleUrl: './add-quiz.component.css'
})
export class AddQuizComponent {
  constructor(private ref:MatDialogRef<AddQuizComponent>,@Inject(MAT_DIALOG_DATA) public data: DialogData,private courseService:CourseService,public router:Router,private quizService:QuizzesService){}
  quizForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    grade: new FormControl('', [Validators.required]),
  });
  closeModal(){
    this.ref.close();
  }
  onsubmit() {
    if (this.quizForm.invalid) {
      return;
    }
    if (this.quizForm.value.description && this.quizForm.value.title && this.quizForm.value.grade) {
    this.quizService.create(Number(this.data.courseId),{
      title:this.quizForm.value.title,
      description:this.quizForm.value.description,
      maxGrade:this.quizForm.value.grade
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


