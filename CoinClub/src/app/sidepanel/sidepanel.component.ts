import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-sidepanel',
  templateUrl: './sidepanel.component.html',
  styleUrls: ['./sidepanel.component.css']
})
export class SidepanelComponent implements OnInit {
  price: string;
  constructor(private _dataService: DataService) {
    this._dataService.getPrice().subscribe(res => (this.price = res['price']));
  }

  ngOnInit() {}
}
