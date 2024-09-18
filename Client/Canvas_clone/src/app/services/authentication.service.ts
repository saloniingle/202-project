import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment.dev";
import {map} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  constructor(private http: HttpClient) {
  }

  login(username:string, password:string ) {
    return this.http.post<any>(environment.apiUrl+ '/login', {username, password})
      .pipe(
        map(result => {
          localStorage.setItem('id_token', result.token);
          localStorage.setItem('user_type', result.user_type);
          localStorage.setItem('user_id', result.id);
          return true;
        })
      );
  }

  logout() {
    localStorage.removeItem("id_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_type");
  }

  get loggedIn(): boolean {
    return (localStorage.getItem('id_token') !== null);
  }
}
