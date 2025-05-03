import { Component } from "@angular/core"
import { ChatService } from "./services/chat.service"
import {CommonModule} from '@angular/common';
import {SidebarComponent} from './components/sidebar/sidebar.component';
import {ChatHeaderComponent} from './components/chat-header/chat-header.component';
import {ChatInputComponent} from './components/chat-input/chat-input.component';
import {InfoSectionComponent} from './components/info-section/info-section.component';
import {TripPlanComponent} from "./components/trip-plan/trip-plan.component";
import {TypingIndicatorComponent} from "./components/typing-indicator/typing-indicator.component";


@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
  standalone: true,
  imports: [
    CommonModule,
    SidebarComponent,
    ChatHeaderComponent,
    ChatInputComponent,
    InfoSectionComponent,
    TripPlanComponent,
    TypingIndicatorComponent
  ]
})
export class AppComponent {
  isMobileSidebarOpen = false

  examples = [
    { text: "Suggest a beach vacation for next month" },
    { text: "What are good destinations for hiking?" },
    { text: "Help me plan a family trip to Europe" },
  ]

  capabilities = [
    { text: "Remembers destinations you've discussed in the conversation" },
    { text: "Can suggest activities based on your interests" },
    { text: "Provides travel tips and recommendations" },
  ]

  limitations = [
    { text: "May occasionally provide outdated travel information" },
    { text: "Cannot book flights or accommodations directly" },
    { text: "Limited knowledge of events after 2023" },
  ]

  constructor(public chatService: ChatService) {}

  toggleMobileSidebar(): void {
    this.isMobileSidebarOpen = !this.isMobileSidebarOpen
  }

  closeMobileSidebar(): void {
    this.isMobileSidebarOpen = false
  }

  handleSendMessage(content: string): void {
    this.chatService.sendMessage(content)
  }
}
