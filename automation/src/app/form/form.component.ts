import { Component, ViewChild, ElementRef,OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { getDocument,GlobalWorkerOptions  } from 'pdfjs-dist';
import { ApiService } from'../service/api.service';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss'],
})
export class FormComponent implements OnInit  {
  formGroup: FormGroup;
  uploading = false;
  selectedFileName: string = '';
  fileContent: ArrayBuffer | undefined;

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  constructor(
    private formBuilder: FormBuilder,
    private apiService:ApiService,
    private router: Router
    ) {
    this.formGroup = this.formBuilder.group({
      title: ['', Validators.required],
      keywords: ['', Validators.required],
    });
  }

  ngOnInit() {
    this.apiService.clearKeyword();
  }

  handleFileInput(event: any): void {
    const file = event.target.files[0];
    console.log('Uploaded file:', file);
    this.selectedFileName = file.name;
    this.readPDFContent(file);
  }
  
  readPDFContent(file: File): void {
    const reader = new FileReader();
    reader.onload = (e) => {
      const bufferArray = reader.result as ArrayBuffer;
      this.parsePDF(bufferArray);
    };
    reader.readAsArrayBuffer(file);
  }
  
  parsePDF(bufferArray: ArrayBuffer): void {
    // Specify the worker source path
    GlobalWorkerOptions.workerSrc = 'pdf.worker.js';
  
    getDocument(bufferArray).promise.then((pdf) => {
      pdf.getPage(1).then((page) => {
        page.getTextContent().then((textContent) => {
          let extractedText = '';
          for (const item of textContent.items) {
            if ((item as any).str) {
              extractedText += (item as any).str + ' ';
            } else if ((item as any).markedContent) {
              extractedText += (item as any).markedContent + ' ';
            }
          }
          console.log('Extracted text:', extractedText);
        });
      });
    });
  }

  onSubmit() {
    if (!this.formGroup.valid) {
      return;      
    }
    this.uploading = true;
  
    const keywords=this.formGroup.get('keywords');
    const title = this.formGroup.get('title');
    console.log(keywords?.value);
    this.apiService.setKeyword(title?.value);
    this.apiService.setKeyword(keywords?.value);
    this.router.navigate(['/result']);
  }

  openFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  clearFile(): void {
    this.selectedFileName = '';
    this.fileInput.nativeElement.value = ''; // Clear the file input value
  }
}
