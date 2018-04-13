import { Component, OnInit, Input } from '@angular/core';
import { NewsService } from './news.service';

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent implements OnInit {
  @Input() news: string;
  constructor(private newsService: NewsService) {}

  ngOnInit() {}
}
