import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeSummaryComponent } from './time-summary.component';

describe('TimeSummaryComponent', () => {
  let component: TimeSummaryComponent;
  let fixture: ComponentFixture<TimeSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TimeSummaryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TimeSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
