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

    this.fetchTransactions(content).subscribe(
      (response: any) => {
        console.log("Response from backend:", response) // 👈 print raw response
        console.log("Coaie", response["prompt-answer"]["response"]["trip_plan"]["accommodation"]["name"].toString())

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response["prompt-answer"]["response"]["trip_plan"]["accommodation"]["name"].toString(),
          role: "assistant",
        }

        this.messages = [...this.messages, botMessage]
      },
      (error) => {
        console.error("Error fetching transactions:", error) // 👈 print error

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
    const body = { "prompt" : prompt }
    return this.http.post(this.backendUrl, body)
  }
}
