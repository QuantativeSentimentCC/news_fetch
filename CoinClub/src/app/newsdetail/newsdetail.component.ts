import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { NewsService } from '../news/news.service';

@Component({
  selector: 'app-newsdetail',
  templateUrl: './newsdetail.component.html',
  styleUrls: ['./newsdetail.component.css']
})
export class NewsdetailComponent implements OnInit {
  news: string;
  href: string;

  constructor(
    private _dataService: DataService,
    private newsService: NewsService
  ) {
    this.href = window.location.href;
    let id = this.href.substr(this.href.lastIndexOf('/') + 1);
    this._dataService.getNewsById(id).subscribe(res => (this.news = res));
  }

  ngOnInit() {}
}
