import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {catchError, map, throwError} from "rxjs";

export interface CoursePayload{
  name: string;
  semester: string;
  faculty_id:number;
  year:number,
  published_status:boolean
}
interface FacultyList {   first_name:string,   id:number,   last_name: string,   username: string }

export interface SyllabusPayLoad{
  "syllabusContent":string;
}

export interface Syllabus{ 
"SyllabusID":number,
"CourseID":number,
"Content":string,
}

export interface Course{
  "courseID": number,
  "name": string,
  "semester": string,
  "year": number,
  "facultyID": number,
  "isPublished":boolean
}

@Injectable({
  providedIn: 'root'
})

export class CourseService {
  constructor(private http: HttpClient) {
  }

  create(coursePayload: CoursePayload){
    return this.http.post(environment.apiUrl+ '/courses', coursePayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  createSyllabus(courseId:number,syllabusPayload:SyllabusPayLoad){
    return this.http.post(environment.apiUrl+ `/courses/${courseId}/syllabus`, syllabusPayload)
      .pipe(
        map(result =>{
          return { result, message: 'Syllabus added successfully.' };
        }),
        catchError((err) =>{return throwError(()=>err)})
      ); 
  }

  getCoursesForAdmin(semester:string, facultyID:number, year:number){
    return this.http.get<Course[]>(environment.apiUrl+ `/courses?semester=${semester}&facultyID=${facultyID}&year=${year}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  getCoursesForStudent(){
    return this.http.get<Course[]>(environment.apiUrl+ `/courses`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  getCoursesForFaculty(facultyID:number){
    return this.http.get<Course[]>(environment.apiUrl+ `/courses?facultyID=${facultyID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  getCourses(semester:string, year:number, isPublished:boolean){
    return this.http.get(environment.apiUrl+ `/courses?semester=${semester}&year=${year}&isPublished=${isPublished}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  getById(courseId:number){
    return this.http.get<Course>(environment.apiUrl+ `/courses/${courseId}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{
          return throwError(()=>err)
        })
      );
  }
  getSyllabusByCourseId(courseId:number){
    return this.http.get<Syllabus>(environment.apiUrl+`/courses/${courseId}/syllabus`)
    .pipe(
      map(result => {
        return result
      }),
      catchError((err) =>{return throwError(()=>err)})
    );
    
      }

  getStudentsByCourse(courseId:number){
    return this.http.get(environment.apiUrl+ `/courses/${courseId}/students`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) =>{return throwError(()=>err)})
      );
  }

  getFaculties(){
    return this.http.get<FacultyList[]>(environment.apiUrl+ `/faculty/`)
      .pipe(
        map(result => {
          return result
        }),
        catchError((err) => {return throwError(()=>err)})
      );
  }

}
