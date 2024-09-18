import {ChangeDetectorRef, Component, Inject, OnInit} from '@angular/core';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatListModule} from "@angular/material/list";
import {MediaMatcher} from "@angular/cdk/layout";
import {Router, RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";
import {AuthenticationService} from "../services/authentication.service";
import {NgxSpinnerService} from "ngx-spinner";
import {CommonModule, DOCUMENT} from "@angular/common";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MatToolbarModule, MatButtonModule, MatIconModule, MatSidenavModule, MatListModule, RouterOutlet, RouterLink, CommonModule, RouterLinkActive,],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent  {

  mobileQuery: MediaQueryList;

  userType:string|null;

  userToken: string | null ;

  sideNavOptions: { isActive: boolean, link: string }[] = [];
  
  private _mobileQueryListener: () => void;

  constructor(@Inject(DOCUMENT) private document: Document, changeDetectorRef: ChangeDetectorRef, media: MediaMatcher,
              protected authenticationService:AuthenticationService,
              private spinner: NgxSpinnerService,
              private router: Router) {
    const localStorage = document.defaultView?.localStorage;
    if(localStorage){
      this.userToken = localStorage?.getItem("id_token") || null;
    }
    if(localStorage?.getItem('user_type')){
      this.userType = localStorage.getItem('user_type')
    }
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
    this.populateSideNavOptions();
  }
  
  logout(): void {
    this.authenticationService.logout();
    this.router.navigateByUrl('/login');
  }

  populateSideNavOptions(): void {
    
    this.sideNavOptions = [];
    this.sideNavOptions.push({ isActive: false, link: "courses" });
    if (this.userType !== 'faculty') {
      this.sideNavOptions.push({ isActive: false, link: "profile" });
    }
  }
}
