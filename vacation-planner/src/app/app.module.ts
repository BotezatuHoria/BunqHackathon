import { NgModule } from "@angular/core"
import { BrowserModule } from "@angular/platform-browser"
import { FormsModule } from "@angular/forms"

import { AppComponent } from "./app.component"
import { SidebarComponent } from "./components/sidebar/sidebar.component"
import { ChatHeaderComponent } from "./components/chat-header/chat-header.component"
import { ChatInputComponent } from "./components/chat-input/chat-input.component"
import { InfoSectionComponent } from "./components/info-section/info-section.component"
import { ChatService } from "./services/chat.service"
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {TripPlanComponent} from "./components/trip-plan/trip-plan.component";
import {TypingIndicatorComponent} from "./components/typing-indicator/typing-indicator.component";

@NgModule({
  declarations: [ ],
  imports: [InfoSectionComponent, SidebarComponent, ChatHeaderComponent, ChatInputComponent, TripPlanComponent, TypingIndicatorComponent, CommonModule, BrowserModule, FormsModule, HttpClientModule],
  providers: [ChatService],
  // bootstrap: [AppComponent],
})
export class AppModule {}
