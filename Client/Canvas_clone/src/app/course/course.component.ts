import { Component, OnInit,Inject } from '@angular/core';
import { CourseService, Syllabus,Course } from '../services/course.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule, DOCUMENT } from '@angular/common';
import { AddSylabbusComponent } from '../add-sylabbus/add-sylabbus.component';
import { MatDialog } from '@angular/material/dialog';
import { MatButton } from '@angular/material/button';
import {NotifierModule, NotifierService} from "angular-notifier";


@Component({
  selector: 'app-course',
  standalone: true,
  imports: [CommonModule,AddSylabbusComponent,MatButton, NotifierModule],
  templateUrl: './course.component.html',
  styleUrl: './course.component.css'
})



export class CourseComponent implements OnInit {
  students: any[] = [];
  sylabbus: Syllabus|null = null;
  courseId:any;
  course: Course;
  content:string;
  userType:string|null;

  private readonly notifier: NotifierService;


  constructor(@Inject(DOCUMENT) private document: Document,public courseService: CourseService,private route: ActivatedRoute,private dialog:MatDialog) {

      const localStorage = document.defaultView?.localStorage;

      if(localStorage?.getItem('user_type')){
        this.userType = localStorage.getItem('user_type')
      }
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      if(params.get('courseID')){
        this.courseId = params.get('courseID')
      }
    });
    if(this.userType=='faculty' || this.userType=='admin'){
      this.loadStudentsByCourse();
    }

    if(this.userType=='faculty' ||  this.userType=="student"){
      this.loadSyllabusByCourseId()
    }
    this.loadgetById();

  }
   openModal(){
    const dialogRef =this.dialog.open(AddSylabbusComponent,{data:{ courseId:this.courseId},
      width:'60%',
    })
    dialogRef.afterClosed().subscribe(result => {
      this.loadSyllabusByCourseId();
    });
   }



  loadStudentsByCourse() {
    this.courseService.getStudentsByCourse(this.courseId).subscribe({
      next: (result: any)=>{
        this.students = result;
        console.log(result)
      },
      error: (err) => {
        this.notifier.notify('error', 'Error occurred loading students');
        console.log(err)
      }
    })}

    loadSyllabusByCourseId(){
    this.courseService.getSyllabusByCourseId(this.courseId).subscribe({
      next: (result:any)=>{
        this.sylabbus = result;
      },
      error: (err) => {
        console.log(err)
        this.notifier.notify('error', 'Error occurred loading syllabus');

      }})}

  loadgetById(){
    this.courseService.getById(this.courseId)
    .subscribe({
      next:(result:any)=>{
        this.course= result;
      },
      error: (err) => {
        this.notifier.notify('error', 'Error occurred loading course');
        console.log(err)
  }})
  }
}


