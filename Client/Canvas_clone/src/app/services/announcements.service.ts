import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {catchError, map, throwError} from "rxjs";


interface AnnouncementPayload{
  announcementText: string;
}

export interface Announcement{
  announcementID:number,
  courseID:number,
  announcementText : string,
  datePosted:string
}

@Injectable({
  providedIn: 'root'
})
export class AnnouncementsService {

  constructor(private http: HttpClient) {
  }

  getAll(courseID:number){
    return this.http.get<Announcement[]>(environment.apiUrl+ `/courses/${courseID}/announcements`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  get(courseID:number, announcementID:number){
    return this.http.get(environment.apiUrl+ `/courses/${courseID}/announcements/${announcementID}`)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

create(courseID:number, announcementPayload: AnnouncementPayload ){
    return this.http.post(environment.apiUrl+ `/courses/${courseID}/announcement`, announcementPayload)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }
}
