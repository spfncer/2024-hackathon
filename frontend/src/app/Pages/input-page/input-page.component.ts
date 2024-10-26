import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { StepperModule } from 'primeng/stepper';
import { InputTextModule } from 'primeng/inputtext';
import { ToggleButtonModule } from 'primeng/togglebutton';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'input-page',
    templateUrl: './input-page.component.html',
    standalone: true,
    imports: [
      StepperModule,
      ButtonModule,
      InputTextModule,
      ToggleButtonModule,
      IconFieldModule,
      InputIconModule,
      FormsModule,
      CommonModule
    ]
})
export class InputPage {
    activeStep: number = 1;


    
}