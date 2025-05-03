import { Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { Observable } from "rxjs"

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

  private userId = 1880854
  private backendUrl = `http://127.0.0.1:8000/users/${this.userId}/transactions`

  constructor(private http: HttpClient) {}

  sendMessage(content: string): void {
    if (!content.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: "user",
    }

    this.messages = [...this.messages, userMessage]

    // POST the user's message to backend
    this.fetchTransactions(content).subscribe(
      (response: any) => {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response.reply ?? `Received ${response.length} transactions.`, // Customize depending on your backend response
          role: "assistant",
        }

        this.messages = [...this.messages, botMessage]
      },
      (error) => {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: `Failed to fetch transactions: ${error.message}`,
          role: "assistant",
        }

        this.messages = [...this.messages, botMessage]
      }
    )
  }

  private fetchTransactions(prompt: string): Observable<any> {
    const body = { prompt }
    return this.http.post(this.backendUrl, body)
  }
}
