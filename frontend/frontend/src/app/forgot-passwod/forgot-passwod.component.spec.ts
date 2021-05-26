import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ForgotPasswodComponent } from './forgot-passwod.component';

describe('ForgotPasswodComponent', () => {
  let component: ForgotPasswodComponent;
  let fixture: ComponentFixture<ForgotPasswodComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ForgotPasswodComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ForgotPasswodComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
