import { Component,Inject,OnInit } from '@angular/core';
import { Course, CourseService } from '../services/course.service';
import { DOCUMENT ,CommonModule} from '@angular/common';
import{MatButton} from '@angular/material/button';
import { AddQuizComponent } from '../add-quiz/add-quiz.component';
import{Quiz, QuizzesService} from '../services/quizzes.service';
import { MatDialog ,MatDialogModule} from '@angular/material/dialog';
import{NgxSpinnerService} from 'ngx-spinner';
import { ActivatedRoute } from '@angular/router';
import{NgxSpinnerModule} from 'ngx-spinner';

@Component({
  selector: 'app-quizzes',
  standalone: true,
  imports: [CommonModule,MatButton,MatDialogModule,NgxSpinnerModule],
  templateUrl: './quizzes.component.html',
  styleUrl: './quizzes.component.css'
})
export class QuizzesComponent  implements OnInit{
  userType:string|null;
  courseId:any;
  quizId:number;
  course: Course;
  quizzes:Quiz[];

  constructor(@Inject(DOCUMENT) private document: Document,public courseService: CourseService,private dialog:MatDialog,private quizzesService:QuizzesService,private spinner:NgxSpinnerService,private route:ActivatedRoute) {

    const localStorage = document.defaultView?.localStorage;

    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }


}
ngOnInit(): void {
  this.courseId = this.document.location.pathname.split('/')[2];
  this.quizId = Number(this.document.location.pathname.split('/')[4]);
  if(this.courseId!=null){this.courseById();
  this.getAllQuizzes();}
}

courseById(){
  this.courseService.getById(this.courseId)
  .subscribe({
    next:(result:any)=>{

      this.course= result;
    },
    error: (err) => {
      console.log(err)
    }})
}
openModal(){
  const dialogRef=this.dialog.open(AddQuizComponent,{data:{ courseId:this.courseId},
    width:'60%',
  })
  dialogRef.afterClosed().subscribe(result => {
    this.getAllQuizzes();
  });
}

getAllQuizzes(){
  this.quizzesService.getAll(Number(this.courseId)).subscribe({
    next: (result: any) => {
      this.quizzes = result;
      console.log(result)
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
