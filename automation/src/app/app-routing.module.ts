import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TableComponent } from './table/table.component';
import { FormComponent } from './form/form.component';
const routes: Routes = [
  { path: 'form', component: FormComponent },
  { path: 'result', component: TableComponent },
  { path: '', redirectTo: '/form', pathMatch: 'full' }, // Default route to the form
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
