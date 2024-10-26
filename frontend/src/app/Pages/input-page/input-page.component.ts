import { Component } from '@angular/core';
import { CardModule } from 'primeng/card';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { StepperModule } from 'primeng/stepper';
import { InputTextModule } from 'primeng/inputtext';
import { ToggleButtonModule } from 'primeng/togglebutton';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { InputNumberModule } from 'primeng/inputnumber';
import { SelectButtonModule } from 'primeng/selectbutton';
import { FloatLabelModule } from 'primeng/floatlabel';
import { FormsModule, FormBuilder } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Validators } from '@angular/forms';

import { InputGroupModule } from 'primeng/inputgroup';
import { InputGroupAddonModule } from 'primeng/inputgroupaddon';

@Component({
  selector: 'input-page',
  templateUrl: './input-page.component.html',
  styleUrls: ['./input-page.component.css'],
  standalone: true,
  imports: [
    StepperModule,
    CardModule,
    AvatarModule,
    ButtonModule,
    InputTextModule,
    ToggleButtonModule,
    IconFieldModule,
    InputIconModule,
    InputNumberModule,
    SelectButtonModule,
    FloatLabelModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    InputGroupModule,
    InputGroupAddonModule
  ]
})
export class InputPage {
  activeStep: number = 1

  // 3 form groups, one per section
  profileForm
  evacuationDataForm
  miscDataForm

  residenceTypeOptions: any[] = [
    { name: 'House', value: 'House' },
    { name: 'Apartment', value: 'Apartment' },
    { name: 'Dorm', value: 'Dorm' }
  ];

  travelOptions: any[] = [
    { name: 'Car', value: 'Car' },
    { name: 'Bus', value: 'Bus' },
    { name: 'Walk', value: 'Walk' }
  ];


  constructor(private formBuilder: FormBuilder) {
    this.profileForm = this.formBuilder.group({
      address: ['', Validators.required],
      residence_type: ['House', Validators.required],
      number_people: [Number(0), [Validators.required, Validators.min(0), Validators.max(100)]]
    });

    this.evacuationDataForm = this.formBuilder.group({
      outside_location: [Boolean(true), Validators.required],
      outside_hotel: [Boolean(true)],
      travel_mode: ['Car', Validators.required]
    });

    this.miscDataForm = this.formBuilder.group({
      small_pets: [Number(0), [Validators.required, Validators.min(0), Validators.max(100)]],
      medium_pets: [Number(0), [Validators.required, Validators.min(0), Validators.max(100)]],
      large_pets: [Number(0), [Validators.required, Validators.min(0), Validators.max(100)]],
      medication: [Boolean(true), Validators.required],
      equipment: [Boolean(true), Validators.required]
    })
  }

  onSubmit() {
    // TODO: Grab the values out of the forms and run a request using the service...
  }
}