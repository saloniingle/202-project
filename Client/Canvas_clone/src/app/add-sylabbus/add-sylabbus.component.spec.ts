import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddSylabbusComponent } from './add-sylabbus.component';

describe('AddSylabbusComponent', () => {
  let component: AddSylabbusComponent;
  let fixture: ComponentFixture<AddSylabbusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddSylabbusComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AddSylabbusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
