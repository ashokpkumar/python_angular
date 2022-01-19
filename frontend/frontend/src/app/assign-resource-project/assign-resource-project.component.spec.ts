import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignResourceProjectComponent } from './assign-resource-project.component';

describe('AssignResourceProjectComponent', () => {
  let component: AssignResourceProjectComponent;
  let fixture: ComponentFixture<AssignResourceProjectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AssignResourceProjectComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssignResourceProjectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
