export interface TripPlan {
  trip_plan: {
    destination: string
    duration_days: number | null
    duration_nights: number | null
    budget: number | null
    current_savings: number | null
    accommodation: {
      name: string
      link: string
      total_cost: number | null
      cost_per_night: number | null
    }
    transportation: {
      suggested_airlines: Array<{
        name: string
        link: string
      }>
      departure_airport: string
      arrival_airport: string
      estimated_cost_range: {
        min: number | null
        max: number | null
      }
    }
    activities_and_food: {
      daily_cost_range: {
        min: number | null
        max: number | null
      }
      suggested_activities: string[]
      suggested_foods: string[]
    }
    total_estimated_cost_range: {
      min: number | null
      max: number | null
    }
    budget_adjustments: string[]
    additional_tips: string[]
  }
}
