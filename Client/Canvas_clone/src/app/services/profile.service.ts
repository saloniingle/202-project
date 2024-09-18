import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {catchError, map, throwError} from "rxjs";

interface ProfilePayload{
  firstname:string;
  lastname:string;
  username:string;
}
@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  constructor(private http: HttpClient) {
  }

  get() {
    var urlString = environment.apiUrl+ `/profile`;
    console.log("urlString", urlString);

    return this.http.get(urlString)
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );
  }

  put(username: string, isNotificationEnabled: boolean, firstname: string, lastname: string) {
    var urlString = environment.apiUrl+ `/profile`;

    return this.http.put(urlString, {"username": username, "notification": isNotificationEnabled, "firstname": firstname, "lastname": lastname})
      .pipe(
        map(result => {
          return result
        }),
        catchError(err => throwError(err))
      );

  }
}
