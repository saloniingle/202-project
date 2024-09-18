import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {catchError, map, throwError} from "rxjs";

interface QuizPayload{
  title:string;
  description:string;
  maxGrade:string;
}
export interface Quiz{
  id:number,
  title : string,
}
interface AssignGradePayload{
  student_grades:number;
  enrollment_id:number
}

export interface QuizInfo{
  "quizId": string,
  "courseId": number,
  "description": string,
  "maxGrade": number,
  "title": string,
}

interface QuizResponseStudent{
  quizInfo:QuizInfo,
  studentGrades: {
    "quizId": number,
    "enrollmentId": number,
    "grade": number,
    "gradeId": number,
    "maxGrade": number
  }
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

interface QuizResponse{
  quizInfo:QuizInfo,
  studentGrades:StudentsGrade[]
}


@Injectable({
  providedIn: 'root'
})
export class QuizzesService {

  constructor(private http: HttpClient) {
  }

  getAll(courseID:number){
    return this.http.get<Quiz[]>(environment.apiUrl+ `/courses/${courseID}/quizzes`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  get(courseID:number, quizID:number){
    return this.http.get(environment.apiUrl+ `/courses/${courseID}/quizzes/${quizID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  getForStudent(courseID:number, quizID:number){
    return this.http.get<QuizResponseStudent>(environment.apiUrl+ `/courses/${courseID}/quizzes/${quizID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }
  create(courseID:number, quizPayload: QuizPayload ){
    return this.http.post(environment.apiUrl+ `/courses/${courseID}/quizzes`, quizPayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }
  assignGrade(courseID:number, quizID:number, assignGradePayload: AssignGradePayload ){
    return this.http.post(environment.apiUrl+ `/courses/${courseID}/quiz/${quizID}/grades`, assignGradePayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }


}
