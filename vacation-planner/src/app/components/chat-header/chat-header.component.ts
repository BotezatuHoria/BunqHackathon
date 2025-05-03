import { Component, Output, EventEmitter } from "@angular/core"
import {CommonModule, NgOptimizedImage} from '@angular/common';

@Component({
  selector: "app-chat-header",
  templateUrl: "./chat-header.component.html",
  styleUrls: ["./chat-header.component.scss"],
  standalone: true,
  imports: [CommonModule, NgOptimizedImage],
})
export class ChatHeaderComponent {
  @Output() menuClick = new EventEmitter<void>()
}
