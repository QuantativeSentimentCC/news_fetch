import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class NewsService {
  //private newsSource = new BehaviorSubject<string>('default news');
  //currentNews = this.newsSource.asObservable();

  constructor() {}

  getNewsDetailLink(id: string) {
    let uri = 'detail?news_id=' + id;
    return uri;
  }

  truncateText(text: string, maxLength) {
    if (text.length > maxLength) {
      text = text.substr(0, maxLength) + '...';
    }
    return text;
  }

  timeConverter(unix_timestamp) {
    var date = new Date(unix_timestamp * 1000);
    var year = date.getFullYear();
    var months = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ];
    var month = months[date.getMonth()];
    var day = '0' + date.getDate();
    var hours = date.getHours();
    var minutes = '0' + date.getMinutes();
    var seconds = '0' + date.getSeconds();
    var formattedTime =
      month +
      '/' +
      day.substr(-2) +
      '/' +
      year +
      ' ' +
      hours +
      ':' +
      minutes.substr(-2) +
      ':' +
      seconds.substr(-2);
    return formattedTime;
  }

  /*changeNews(news: string) {
    this.newsSource.next(news);
  }*/
}
