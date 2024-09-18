import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {catchError, map, throwError} from "rxjs";

interface AssignmentPayload{
  title:string;
  description:string;
  maxGrade:string;
}

interface AssignGradePayload{
  student_grades:number;
  enrollment_id:number
}

export interface Assignment{
  id:number,
  title : string,
}

export interface AssignmentInfo{
  "assignmentId": string,
  "courseId": number,
  "description": string,
  "maxGrade": number,
  "title": string
}

export interface StudentsGrade{
  "assignmentId": null,
  "enrollmentId": number,
  "firstName": string,
  "grade": string|null,
  "gradeId": string | null,
  "lastName": string,
  "maxGrade": number,
  "studentId": number,
  "username"?: string
}

interface AssignmentResponse{
  assignmetInfo:AssignmentInfo,
  studentGrades:StudentsGrade[]
}

interface AssignmentResponseStudent{
  assignmetInfo:AssignmentInfo,
  studentGrades: {
    "assignmentId": number,
    "enrollmentId": number,
    "grade": number,
    "gradeId": number,
    "maxGrade": number
  }
}
@Injectable({
  providedIn: 'root'
})
export class AssignmentsService {

  constructor(private http: HttpClient) {
  }

  getAll(courseId:number){
    return this.http.get<Assignment[]>(environment.apiUrl+ `/courses/${courseId}/assignments`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  get(courseID:number, assignmentID:number){
    return this.http.get<AssignmentResponse>(environment.apiUrl+ `/courses/${courseID}/assignments/${assignmentID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  getForStudent(courseID:number, assignmentID:number){
    return this.http.get<AssignmentResponseStudent>(environment.apiUrl+ `/courses/${courseID}/assignments/${assignmentID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  create(courseID:number, assignmentPayload: AssignmentPayload ){
    return this.http.post(environment.apiUrl+ `/courses/${courseID}/assignments`, assignmentPayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  assignGrade(courseID:number, assignmentID:number, assignGradePayload: AssignGradePayload ){
    return this.http.post(environment.apiUrl+ `/courses/${courseID}/assignment/${assignmentID}/grades`, assignGradePayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }
}
