import { TestBed } from '@angular/core/testing';
import { InputPage } from './input-page.component';

describe('InputPage', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InputPage],
    }).compileComponents();
  });

  it('should create the page', () => {
    const fixture = TestBed.createComponent(InputPage);
    const page = fixture.componentInstance;
    expect(page).toBeTruthy();
  });
});
