import { Component, ViewChild, OnInit  } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort } from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { ApiService } from'../service/api.service';
import { AutomationData } from '../service/api.data';
/**
 * @title Data table with sorting, pagination, and filtering.
 */
@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit  {
  dataSource = new MatTableDataSource<AutomationData>();
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  displayedColumns: string[] = ['No','title', 'similarity', 'icon'];
  constructor(    
    private apiService:ApiService,
    ){}

  ngOnInit() {  
    this.apiService.getData('python ')
      .subscribe(
        (data: AutomationData[]) => {
          // This block of code will be executed when data is emitted by the observable
          console.log(data);
          this.dataSource = new MatTableDataSource<AutomationData>(data);
          // Handle the 'data' here as needed
        },
        (error) => {
          // Handle errors here if any
          console.error(error);
        }
      );
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  onOpenClick(data:any):void{
    console.log(data);

  }
}
