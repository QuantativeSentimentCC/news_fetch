const express = require('express');
const router = express.Router();
const MongoClient = require('mongodb').MongoClient;
const ObjectID = require('mongodb').ObjectID;

/* Connect
const connection = closure => {
  return MongoClient.connect('mongodb://localhost:27017/cs5412', (err, db) => {
    if (err) return console.log(err);

    closure(db);
  });
};*/

// Error handling
const sendError = (err, res) => {
  response.status = 501;
  response.message = typeof err == 'object' ? err.message : err;
  res.status(501).json(response);
};

// Response handling
let response = {
  status: 200,
  data: [],
  message: null
};

// Get news
router.get('/news', (req, res) => {
  MongoClient.connect('mongodb://localhost:27017', (err, client) => {
    if (err) throw err;
    client
      .db('cs5412')
      .collection('news_data')
      .find({})
      .sort({ time: -1 })
      .toArray()
      .limit(20)
      .then(news => {
        response.data = news;
        res.json(response);
      })
      .catch(err => {
        sendError(err, res);
      });
  });
});

router.get('/news/:news_id', (req, res) => {
  MongoClient.connect('mongodb://localhost:27017', (err, client) => {
    if (err) throw err;
    client
      .db('cs5412')
      .collection('news_data')
      .findOne({ _id: ObjectID(req.params.news_id) })
      .then(news => {
        response.data = news;
        res.json(response);
      })
      .catch(err => {
        sendError(err, res);
      });
  });
});

module.exports = router;
