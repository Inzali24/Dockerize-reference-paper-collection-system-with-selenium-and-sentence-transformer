import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AutomationData } from './api.data';
import { map } from 'rxjs/operators';
import { Observable , of } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  formData: string[]=[];
  private apiUrl = 'http://localhost:5001/'; // Replace with your Flask API URL for docker
  //private apiUrl = 'http://127.0.0.9:8080/'; // Replace with your Flask API URL for local

  constructor(private http: HttpClient) {}

  setKeyword(keyword: string){
     this.formData.push(keyword);
  }

  getKeyword():string[]{
    return this.formData;
  }

  clearKeyword(){
    this.formData=[];
  }

   getData(keywords: string[]):  Observable<AutomationData[]> {
    if(keywords.length==0){
      return of([]);
    }
    const url = `${this.apiUrl}/getdata?keywords=${keywords[1]}&title=${keywords[0]}`;
    return this.http.get<AutomationData[]>(url)
      .pipe(
        map((response: any) => {    
          return response as AutomationData[];
        })
      );
  }
}
