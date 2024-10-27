import { Component } from '@angular/core';
import { Card, CardModule } from 'primeng/card';

@Component({
  selector: 'output-page',
  templateUrl: './output-page.component.html',
  styleUrls: ['./output-page.component.css'],
  standalone: true,
  imports: [CardModule],
})
export class OutputPage {}
