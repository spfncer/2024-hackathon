import { Routes } from '@angular/router';
import { InputPage } from './Pages/input-page/input-page.component';
import { OutputPage } from './Pages/output-page/output-page.component';

export const routes: Routes = [
  { path: 'output', component: OutputPage },
  { path: '**', component: InputPage },
];
