import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SparkleYourLifeComponent } from './sparkle-your-life.component';

describe('SparkleYourLifeComponent', () => {
  let component: SparkleYourLifeComponent;
  let fixture: ComponentFixture<SparkleYourLifeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SparkleYourLifeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SparkleYourLifeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
