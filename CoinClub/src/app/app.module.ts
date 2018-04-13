import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { TitleComponent } from './title/title.component';
import { NewsComponent } from './news/news.component';
import { NewslistComponent } from './newslist/newslist.component';
import { NewsdetailComponent } from './newsdetail/newsdetail.component';

import { HttpModule } from '@angular/http';
import { DataService } from './data.service';
import { NewsService } from './news/news.service';
import { Routes, RouterModule, Router } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SidepanelComponent } from './sidepanel/sidepanel.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'home/detail/:id', component: NewsdetailComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    NewsComponent,
    NewslistComponent,
    TitleComponent,
    NewsdetailComponent,
    HomeComponent,
    SidepanelComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes, { useHash: true })
  ],
  providers: [DataService, NewsService],
  bootstrap: [AppComponent]
})
export class AppModule {}
