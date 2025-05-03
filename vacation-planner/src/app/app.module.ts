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

@NgModule({
  declarations: [ ],
  imports: [InfoSectionComponent, SidebarComponent, ChatHeaderComponent, ChatInputComponent, CommonModule, BrowserModule, FormsModule],
  providers: [ChatService],
  bootstrap: [AppComponent],
})
export class AppModule {}
