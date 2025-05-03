import { Component, Output, EventEmitter } from "@angular/core"
import {CommonModule} from '@angular/common';

@Component({
  selector: "app-chat-header",
  templateUrl: "./chat-header.component.html",
  styleUrls: ["./chat-header.component.scss"],
  standalone: true,
  imports: [CommonModule],
})
export class ChatHeaderComponent {
  @Output() menuClick = new EventEmitter<void>()
}
