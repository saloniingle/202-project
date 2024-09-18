import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi} from "@angular/common/http";
import {AuthInterceptor} from "./interceptor/auth.interceptor";
import {provideAnimations} from "@angular/platform-browser/animations";
import {AuthGuard} from "./guards/auth.guard";

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideClientHydration(), provideAnimations(), provideAnimationsAsync(), provideHttpClient(
    withInterceptorsFromDi()
  ),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    }, AuthGuard]
};
