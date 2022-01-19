import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimesubmissionsComponent } from './timesubmissions.component';

describe('TimesubmissionsComponent', () => {
  let component: TimesubmissionsComponent;
  let fixture: ComponentFixture<TimesubmissionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TimesubmissionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TimesubmissionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
