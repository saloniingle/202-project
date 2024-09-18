import {Component, Inject, inject, OnInit} from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatRadioChange, MatRadioModule} from '@angular/material/radio';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {CommonModule, DOCUMENT} from '@angular/common';
import {Course, CoursePayload, CourseService} from "../services/course.service";
import {NotifierModule, NotifierService} from "angular-notifier";
import { Router } from '@angular/router';
import {NgxSpinnerModule, NgxSpinnerService} from "ngx-spinner";
import {AuthenticationService} from "../services/authentication.service";

type CardContent = {
  id:number,
  title: string;
  description: string;
};

@Component({
  selector: 'app-courses',
  standalone: true,
  templateUrl: './courses.component.html',
  styleUrl: './courses.component.css',
  imports: [MatButtonModule, MatToolbarModule, MatCardModule, FormsModule, MatInputModule, MatSelectModule, MatFormFieldModule, MatRadioModule, MatCheckboxModule, CommonModule, NotifierModule, NgxSpinnerModule]
})
export class CoursesComponent implements OnInit{
  selectedRadioValue: number;
  selectedFacultyID:number;
  selectedSemester:string;
  selectedYear:number;
  courseName: string;
  publishCourse: boolean = false;
  userType:string|null;
  userID:number;
  faculties: { label:string, value:number }[] = []
  courses: Course[] = [];

  private readonly notifier: NotifierService;
  constructor(@Inject(DOCUMENT) private document: Document, private coursesService: CourseService, notifierService: NotifierService, private router:Router, private spinner: NgxSpinnerService, protected authenticationService:AuthenticationService
  ) {
    const localStorage = document.defaultView?.localStorage;

    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }
    if(localStorage?.getItem('user_id')){
      this.userID = Number(localStorage.getItem('user_id'))
    }
    this.notifier = notifierService;
  }

  ngOnInit(): void {
    this.spinner.show()
    if(this.userType=='faculty' && this.userID) {
      this.selectedFacultyID = this.userID;
      this.coursesService.getCoursesForFaculty(this.selectedFacultyID).subscribe({
        next: (result)=> {
          this.courses = result;
          this.spinner.hide();
        },
        error: (err)=>{
          console.log(err)
          this.spinner.hide();
        }
      })
    }
    if(this.userType=='student') {
      this.coursesService.getCoursesForStudent().subscribe({
        next: (result)=> {
          this.courses = result;
          this.spinner.hide();
        },
        error: (err)=>{
          console.log(err)
          this.spinner.hide();
        }
      })
    }
    if(this.userType=='admin') {
      this.coursesService.getFaculties().subscribe({
        next: facultyList => {
          for (const faculty of facultyList) {
            this.faculties.push({label: faculty.first_name + " " + faculty.last_name, value: faculty.id});
          }
          this.spinner.hide();
        },
        error: err => {
          this.notifier.notify('error', 'There is some issue fetching faculty list');
          this.spinner.hide();
        }
      })
    }
  }

  submitCourse() {
    const newCourse:CoursePayload = {
    name: this.courseName,
    semester: this.selectedSemester,
    faculty_id:this.selectedFacultyID,
      year: this.selectedYear,
    published_status:this.publishCourse
  }
    this.spinner.show()
    this.coursesService.create(newCourse).subscribe({
      next: ()=>{
        this.notifier.notify('success', `Created the course ${this.courseName}`);
        this.spinner.hide();
      },
      error:(err)=>{
        this.notifier.notify('error', 'There is some issue creating a course');
        this.spinner.hide();
      }
    })

  }

  searchCourses(){
    this.spinner.show();
    this.coursesService.getCoursesForAdmin(this.selectedSemester,this.selectedFacultyID, this.selectedYear).subscribe({
      next: (result)=> {
        this.courses = result;
        this.spinner.hide();
      },
      error: (err)=>{
        console.log(err)
        this.spinner.hide();
      }
    })

  }

  onChange(event: MatRadioChange) {
    this.selectedRadioValue = event.value;
  }

  isSearchButtonDisabled(){
    if(this.selectedYear && this.selectedSemester && this.selectedFacultyID && this.courseName){
      return false
    }
    return true
  }


  onClick(id:number){
    this.router.navigateByUrl(`courses/${id}`)
  }


}

