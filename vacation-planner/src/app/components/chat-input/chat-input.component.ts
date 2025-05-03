import { Component, Output, EventEmitter } from "@angular/core"
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
  selector: "app-chat-input",
  templateUrl: "./chat-input.component.html",
  styleUrls: ["./chat-input.component.scss"],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class ChatInputComponent {
  @Output() sendMessage = new EventEmitter<string>()

  message = ""

  onSubmit(): void {
    if (this.message.trim()) {
      this.sendMessage.emit(this.message)
      this.message = ""
    }
  }
}
