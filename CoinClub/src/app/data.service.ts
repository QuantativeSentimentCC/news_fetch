import { Injectable } from '@angular/core';

import { Http, Headers, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

@Injectable()
export class DataService {
  result: any;

  constructor(private _http: Http) {}

  getNews() {
    return this._http
      .get('/api/news')
      .map(result => (this.result = result.json().data));
  }

  getNewsById(id: string) {
    return this._http
      .get('/api/news/' + id)
      .map(result => (this.result = result.json().data));
  }

  getPrice() {
    return this._http
      .get('/api/price')
      .map(result => (this.result = result.json().data));
  }

  getHeadlines() {
    return this._http
      .get('/api/headlines')
      .map(result => (this.result = result.json().data));
  }
}
