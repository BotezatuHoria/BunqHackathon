import { Component, Input } from "@angular/core"

import {CommonModule} from '@angular/common';
import {TripPlan} from '../../models/trip-plan.models';

@Component({
  selector: "app-trip-plan",
  templateUrl: "./trip-plan.component.html",
  styleUrls: ["./trip-plan.component.scss"],
  standalone: true,
  imports: [CommonModule],
})
export class TripPlanComponent {
  @Input() tripPlan!: TripPlan

  activeSection = "overview"

  setActiveSection(section: string): void {
    this.activeSection = section === this.activeSection ? "" : section
  }

  isSectionActive(section: string): boolean {
    return this.activeSection === section
  }

  getBudgetPercentage(): number {
    const plan = this.tripPlan.trip_plan
    if (plan.budget && plan.total_estimated_cost_range.max) {
      return Math.min(100, (plan.total_estimated_cost_range.max / plan.budget) * 100)
    }
    return 0
  }

  getSavingsPercentage(): number {
    const plan = this.tripPlan.trip_plan
    if (plan.current_savings && plan.total_estimated_cost_range.min) {
      return Math.min(100, (plan.current_savings / plan.total_estimated_cost_range.min) * 100)
    }
    return 0
  }
}
