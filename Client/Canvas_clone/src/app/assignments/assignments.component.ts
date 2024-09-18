import { Component,Inject,OnInit } from '@angular/core';
import { Course, CourseService } from '../services/course.service';
import { DOCUMENT ,CommonModule} from '@angular/common';
import{MatButton} from '@angular/material/button';
import { AddAssignmentComponent } from '../add-assignment/add-assignment.component';
import { Assignment, AssignmentsService } from '../services/assignments.service';
import { MatDialog ,MatDialogModule} from '@angular/material/dialog';
import{NgxSpinnerService} from 'ngx-spinner';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerModule } from 'ngx-spinner';

@Component({
  selector: 'app-assignments',
  standalone: true,
  imports: [CommonModule,MatButton,MatDialogModule,NgxSpinnerModule],
  templateUrl: './assignments.component.html',
  styleUrl: './assignments.component.css'
})
export class AssignmentsComponent implements OnInit{
  userType:string|null;
  courseId:any|null;
  assignmentId:any|null;
  course: Course;
  assignments:Assignment[];

  constructor(@Inject(DOCUMENT) private document: Document,public courseService: CourseService,private dialog:MatDialog,private assignmentService:AssignmentsService,private spinner:NgxSpinnerService,private route:ActivatedRoute) {

    const localStorage = document.defaultView?.localStorage;

    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }


}
ngOnInit(): void {
  this.spinner.show()
  this.courseId = this.document.location.pathname.split('/')[2];
  this.route.paramMap.subscribe(params => {
    if(params.get('assignmentID')){
      this.assignmentId = params.get('assignmentID')
    }
  }); this.spinner.hide();
  if(this.courseId!=null){this.courseById();
  this.getAllAssignments();}
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
    const dialogRef=this.dialog.open(AddAssignmentComponent,{data:{ courseId:this.courseId},
      width:'60%',
    })
    dialogRef.afterClosed().subscribe(result => {
      this.getAllAssignments();
    });
   }

   getAllAssignments(){
    this.assignmentService.getAll(Number(this.courseId)).subscribe({
      next: (result: any) => {
        this.assignments = result;
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
   getAssignmentById(){
    this.assignmentService.get(Number(this.courseId),Number(this.assignmentId)).subscribe({
      next: (result: any) => {
        this.assignments = result;
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
  onClick(){
    this.getAssignmentById();
  }
}
