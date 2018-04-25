import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {
  defaultUrls: Array<string>;
  headLines: Array<any>;
  constructor(private _dataService: DataService) {
    this.defaultUrls = [
      'https://static01.nyt.com/images/2018/04/25/us/politics/25dc-cfpb1/25dc-cfpb1-facebookJumbo.jpg',
      'https://localtvwtvr.files.wordpress.com/2018/04/subway-dog.jpeg?quality=85&strip=all',
      'https://apple.insidercdn.com/gallery/25791-35675-Image-result-for-site-appleinsidercom-supreme-court-xl.jpg'
    ];
    this._dataService.getHeadlines().subscribe(res => (this.headLines = res));
    console.log(this.headLines);
  }

  ngOnInit() {}
}
