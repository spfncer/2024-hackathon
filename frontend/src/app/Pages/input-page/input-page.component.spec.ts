import { TestBed } from '@angular/core/testing';
import { InputPage } from './input-page.component';

describe('InputPage', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InputPage],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(InputPage);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have the 'frontend' title`, () => {
    const fixture = TestBed.createComponent(InputPage);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('frontend');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(InputPage);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, frontend');
  });
});
