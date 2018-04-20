'use strict';
const mongotocsv = require('mongo-to-csv');
let options = {
  database: 'cs5412', // required
  collection: 'news_data', // required
  fields: ['title', 'time', 'text', 'weight', 'source'], // required
  output: './output/news_data.csv', // required
  allValidOptions: '' // optional
};
mongotocsv.export(options, function(err, success) {
  console.log(err);
  console.log(success);
});
