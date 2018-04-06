import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ServerComponent } from './server/server.component';
import { HeaderComponent } from './header/header.component';
import { NewsComponent } from './news/news.component';
import { NewslistComponent } from './newslist/newslist.component';

@NgModule({
  declarations: [
    AppComponent,
    ServerComponent,
    HeaderComponent,
    NewsComponent,
    NewslistComponent
  ],
  imports: [BrowserModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
