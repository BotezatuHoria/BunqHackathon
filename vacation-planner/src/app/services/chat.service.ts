import { Injectable } from "@angular/core"

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
}

@Injectable({
  providedIn: "root",
})
export class ChatService {
  messages: Message[] = []

  sendMessage(content: string): void {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: "user",
    }

    this.messages = [...this.messages, userMessage]

    // Simulate bot response after a short delay
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm your vacation planning assistant. How can I help you plan your next trip?",
        role: "assistant",
      }

      this.messages = [...this.messages, botMessage]
    }, 1000)
  }
}
