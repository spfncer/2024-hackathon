import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { InputPage } from './Pages/input-page/input-page.component';
import { NavbarComponent } from './components/navbar/navbar.component';

import { PrimeNGConfig } from 'primeng/api';
import { Aura } from 'primeng/themes/aura';
import { OutputPage } from './Pages/output-page/output-page.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, InputPage, NavbarComponent, OutputPage],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'frontend';

  constructor(private primengConfig: PrimeNGConfig) {
    this.primengConfig.theme.set({
      preset: Aura,
      options: {
        darkModeSelector: '.dark-mode'
      }
    });
  }
}
