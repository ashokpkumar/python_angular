import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignProjectResourceComponent } from './assign-project-resource.component';

describe('AssignProjectResourceComponent', () => {
  let component: AssignProjectResourceComponent;
  let fixture: ComponentFixture<AssignProjectResourceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AssignProjectResourceComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssignProjectResourceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
