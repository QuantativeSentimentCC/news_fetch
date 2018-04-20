'use strict';
const mongotocsv = require('mongo-to-csv');
let options = {
  database: 'cs5412', // required
  collection: 'price_data', // required
  fields: ['id', 'price', 'timestamp', 'exchange'], // required
  output: './output/price_data.csv', // required
  allValidOptions: '' // optional
};
mongotocsv.export(options, function(err, success) {
  console.log(err);
  console.log(success);
});
