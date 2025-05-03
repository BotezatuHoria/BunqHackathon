import { bootstrapApplication }  from '@angular/platform-browser';
import { provideRouter }          from '@angular/router';
import { AppComponent }           from './app/app.component';
import {importProvidersFrom} from '@angular/core';
import {appConfig} from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
    // plus any @Injectable providers you need…
.catch(err => console.error(err));
