import { Component, ViewChild, OnInit  } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort } from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { ApiService } from'../service/api.service';
import { SpinnerService } from '../service/spinner.service';
import { AutomationData } from '../service/api.data';
import { DialogService } from '../service/dialog.service';
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
  dataList: AutomationData[]=[];
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  displayedColumns: string[] = ['No','title', 'similarity','citations', 'icon'];
  constructor(    
    private apiService:ApiService,
    public spinnerService:SpinnerService,
    private dialogService:DialogService
    ){}

  async ngOnInit() {  
    const keyword:string[] = this.apiService.getKeyword();
    this.spinnerService.show();
    await this.apiService.getData(keyword)
      .subscribe(
        (data: AutomationData[]) => {
          // This block of code will be executed when data is emitted by the observable
          data.forEach((item, index) => {
            item['No'] = index + 1;
          });
          
          this.dataSource = new MatTableDataSource<AutomationData>(data);
          this.dataSource.paginator = this.paginator;
          this.dataSource.sort = this.sort;
          this.spinnerService.hide();
          // Handle the 'data' here as needed
        },
        (error) => {
          // Handle errors here if any
          this.spinnerService.hide();
          //this.dialogService.openErrorDialog(JSON.stringify(error));
          this.dialogService.openErrorDialog('There is no search results');
          console.error(JSON.stringify(error));
        }
      );
   //this.setTableData();
  }

  setTableData(){
    console.log(this.dataList);
    this.dataSource = new MatTableDataSource<AutomationData>(this.dataList);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  onOpenClick(data:any):void{
    const newTabUrl = `javascript:void(0);window.open('${data}', '_blank');`;
    window.location.href = newTabUrl;
  }
}
