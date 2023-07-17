import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AutomationData } from './api.data';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.9:8080/'; // Replace with your Flask API URL

  constructor(private http: HttpClient) {}

  getData(keywords: string): Observable<AutomationData[]> {
    const url = `${this.apiUrl}/getdata?keywords=${keywords}`;
    return this.http.get<AutomationData[]>(url)
      .pipe(
        map((response: any) => {         
          return response as AutomationData[];
        })
      );
  }
}
