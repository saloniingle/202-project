import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CoursesComponent} from "../courses/courses.component";
import {HomeComponent} from "./home.component";
import{ProfileComponent}from"../profile/profile.component";
import {CourseComponent} from "../course/course.component";
import {AnnouncementsComponent} from "../announcements/announcements.component";
import { AssignmentsComponent } from '../assignments/assignments.component';
import { AssignmentComponent } from '../assignment/assignment.component';
import { QuizzesComponent } from '../quizzes/quizzes.component';
import { QuizComponent } from '../quiz/quiz.component';

export const routes: Routes = [
  { path : '',
    component: HomeComponent,
    children: [
      {
        path: '', component: CoursesComponent
      },
      {
        path: 'courses', component: CoursesComponent
      },
      {
        path: 'profile', component: ProfileComponent
      },
      {
        path: 'courses/:courseID', component: CourseComponent
      },
      {
        path: 'courses/:courseID/announcements', component: AnnouncementsComponent
      },
      {
        path: 'courses/:courseID/assignments', component: AssignmentsComponent
      },
      {
        path: 'courses/:courseID/assignments/:assignmentID', component: AssignmentComponent
      },
      {
        path: 'courses/:courseID/quizzes', component: QuizzesComponent
      },
      {
        path: 'courses/:courseID/quizzes/:quizID', component: QuizComponent
      }
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
