import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-newslist',
  templateUrl: './newslist.component.html',
  styleUrls: ['./newslist.component.css']
})
export class NewslistComponent implements OnInit {
  newsList: Array<any>;
  constructor(private _dataService: DataService) {
    this._dataService.getNews().subscribe(res => (this.newsList = res));
  }

  ngOnInit() {}
}
