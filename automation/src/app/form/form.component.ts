import { Component, ViewChild, ElementRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { getDocument,GlobalWorkerOptions  } from 'pdfjs-dist';
import { ApiService } from'../service/api.service';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss'],
})
export class FormComponent {
  formGroup: FormGroup;
  uploading = false;
  selectedFileName: string = '';
  fileContent: ArrayBuffer | undefined;

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  constructor(
    private formBuilder: FormBuilder,
    private apiService:ApiService,
    ) {
    this.formGroup = this.formBuilder.group({
      title: ['', Validators.required],
      keywords: ['', Validators.required],
    });
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
    console.log(keywords?.value);
    // // Perform form submission or API call    
    // let responseData;
    // this.apiService.getData(keywords?.value).subscribe(
    //   (data) => {
    //     responseData = data;
    //   },
    //   (error) => {
    //     console.error('Error fetching data:', error);
    //   }
    // );
    // console.log(responseData);
  }

  openFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  clearFile(): void {
    this.selectedFileName = '';
    this.fileInput.nativeElement.value = ''; // Clear the file input value
  }
  onNavigate(){

  }
}
