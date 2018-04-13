import { Injectable } from '@angular/core';

import { Http, Headers, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/map';

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
}
