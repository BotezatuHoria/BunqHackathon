import { Component, Input } from "@angular/core"
import {CommonModule} from '@angular/common';

@Component({
  selector: "app-info-section",
  templateUrl: "./info-section.component.html",
  styleUrls: ["./info-section.component.scss"],
  standalone: true,
  imports: [CommonModule],
})
export class InfoSectionComponent {
  @Input() icon = ""
  @Input() title = ""
  @Input() items: { text: string }[] = []
}
