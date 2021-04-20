import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IndividualTimeComponent } from './individual-time.component';

describe('IndividualTimeComponent', () => {
  let component: IndividualTimeComponent;
  let fixture: ComponentFixture<IndividualTimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IndividualTimeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IndividualTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
