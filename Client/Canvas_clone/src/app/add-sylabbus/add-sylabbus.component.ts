import { Component, OnInit,Inject} from '@angular/core';
import {  MatDialogRef ,MAT_DIALOG_DATA, MatDialogContent, MatDialogActions,MatDialogModule} from '@angular/material/dialog';
import { CourseService} from '../services/course.service';
import { ActivatedRoute ,Router} from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
export interface DialogData {
  courseId: string;
}
import {  FormGroup, FormControl, Validators,ReactiveFormsModule} from '@angular/forms';


export interface DialogData {
  courseId: string;
}

@Component({
  selector: 'app-add-sylabbus',
  standalone: true,
  imports: [MatButtonModule,MatDialogContent,MatDialogActions,MatDialogModule,ReactiveFormsModule,],
  templateUrl: './add-sylabbus.component.html',
})

export class AddSylabbusComponent  {
  courseId:any;

  userType:string|null;


  constructor(private ref:MatDialogRef<AddSylabbusComponent>,@Inject(MAT_DIALOG_DATA) public data: DialogData,private route: ActivatedRoute,private courseService:CourseService,public router:Router){}
  syllabusForm = new FormGroup({
    body: new FormControl('', [Validators.required]),
  });

  closeModal(){
    this.ref.close();
  }
  onsubmit() {
    if (this.syllabusForm.invalid) {
      return;
    }
    if (this.syllabusForm.value.body) {
    this.courseService.createSyllabus(Number(this.data.courseId),{
      syllabusContent:this.syllabusForm.value.body})
      .subscribe({
        next:(result)=>{
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


