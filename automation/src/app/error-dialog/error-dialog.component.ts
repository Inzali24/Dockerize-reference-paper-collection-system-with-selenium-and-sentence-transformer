import { Component, OnInit,Inject } from '@angular/core';
import { MAT_DIALOG_DATA,MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-error-dialog',
  templateUrl: './error-dialog.component.html',
  styleUrls: ['./error-dialog.component.scss']
})
export class ErrorDialogComponent implements OnInit {
  errorMessage: string;

  constructor(@Inject(MAT_DIALOG_DATA) 
    public data: { errorMessage: string },  
    private dialogRef: MatDialogRef<ErrorDialogComponent>,
    private router : Router ) {
    this.errorMessage = data.errorMessage;    
  }

  ngOnInit(): void {
  }

  closeDialog(): void {
    this.dialogRef.close();
    this.router.navigate(['form']); // Replace '/target-route' with the route you want to navigate to
  }
}
