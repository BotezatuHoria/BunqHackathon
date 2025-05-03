import {
  Component,
  Input,
  Output,
  EventEmitter,
  HostListener,
  AfterViewInit
} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements AfterViewInit {
  @Input() isOpen = false;
  @Output() close = new EventEmitter<void>();

  isMobile = false;

  chatHistory = [
    { id: 1, title: 'AI Chat Tool Ethics' },
    { id: 2, title: 'AI Chat Tool Impact Writing' },
    { id: 3, title: 'New chat' },
  ];

  // Run only in browser after view is initialized
  ngAfterViewInit(): void {
    this.checkScreenSize();
  }

  @HostListener('window:resize')
  checkScreenSize(): void {
    if (typeof window !== 'undefined') {
      this.isMobile = window.innerWidth < 768;
      if (!this.isMobile && this.isOpen) {
        this.close.emit();
      }
    }
  }

  removeChat(id: number): void {
    this.chatHistory = this.chatHistory.filter((chat) => chat.id !== id);
  }
}
