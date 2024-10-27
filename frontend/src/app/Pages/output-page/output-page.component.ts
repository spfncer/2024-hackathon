import { Component, computed, effect, signal } from '@angular/core';
import { CardModule } from 'primeng/card';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { httpSignal } from '../../utils/httpSignal';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { SparkleYourLifeComponent } from '../../components/sparkle-your-life/sparkle-your-life.component';
import { of } from 'rxjs';

@Component({
  selector: 'output-page',
  templateUrl: './output-page.component.html',
  styleUrls: ['./output-page.component.css'],
  standalone: true,
  imports: [CardModule, ProgressSpinnerModule, SparkleYourLifeComponent],
})
export class OutputPage {
  state = signal({});

  statusHeader = computed(() => {
    switch (this.status()?.status) {
      case 'okay':
        return 'Prepare to Shelter in Place';
      case 'be-prepared':
        return 'Be Prepared to Evacuate';
      case 'evacuate':
        return 'Evacuate Now';
      default:
        return 'Loading...';
    }
  });

  statusMessage = computed(() => {
    switch (this.status()?.status) {
      case 'okay':
        return 'The current conditions are potentially dangerous but mitigatable. Be prepared to shelter in place and watch for updates from local authorities.';
      case 'be-prepared':
        return 'The current conditions are potentially dangerous. Be prepared to evacuate if the situation changes and watch for updates from local authorities.';
      case 'evacuate':
        return 'The current conditions are extremely dangerous. Evacuate immediately.';
      default:
        return '...';
    }
  });

  status = httpSignal(() => {
    return this.httpClient.get<any>(
      //@ts-expect-error
      `http://localhost:8000/status/${this.state()?.address}`,
      {}
    );
  });

  hotels = httpSignal(() => {
    //@ts-expect-error
    if (this.state()?.address && this.state()?.outside_hotel) {
      return this.httpClient.get<any>(
        //@ts-expect-error
        `http://localhost:8000/hotels/${this.state().address}`,
        {}
      );
    } else {
      return of(null); // Return an observable of null if address is not present
    }
  });

  guidance = httpSignal(() => {
    return this.httpClient.get<any>(
      `http://localhost:8000/results/${JSON.stringify(this.state())}`,
      {}
    );
  });

  constructor(private router: Router, private httpClient: HttpClient) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.state.set(navigation.extras.state);
      console.log(this.state());
    }
    effect(() => {
      // console.log(this.state());
    });
  }
}
