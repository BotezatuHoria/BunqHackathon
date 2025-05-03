import { Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { Observable } from "rxjs"
import {TripPlan} from "../models/trip-plan.models";

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  tripPlan?: TripPlan
}

@Injectable({
  providedIn: "root",
})
export class ChatService {
  messages: Message[] = []
  isLoading = false // property to track loading state

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

    this.isLoading = true

    this.fetchTransactions(content).subscribe(
      (response: any) => {
        console.log("Response from backend:", response) // 👈 print raw response

        this.isLoading = false

        try {
          const tripPlanData = response["prompt-answer"]["response"]

          // Create a properly formatted trip plan object
          const tripPlan: TripPlan = {
            trip_plan: tripPlanData.trip_plan,
          }

          const botMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: "Here is your trip plan:",
            role: "assistant",
            tripPlan: tripPlan,
          }

          this.messages = [...this.messages, botMessage]
        } catch (error) {
          console.error("Error processing trip plan:", error) // 👈 print error

          const botMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: "I couldn't process your trip plan. Please try again.",
            role: "assistant",
          }

          this.messages = [...this.messages, botMessage]
        }
      },
      (error) => {
        console.error("Error fetching transactions:", error) // 👈 print error

        this.isLoading = false

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
