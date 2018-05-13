#!/usr/bin/python3

import requests
import pprint
import feedparser
import requests
import json
import dateutil.parser as dp
from pymongo import MongoClient
import hashlib
from time import sleep
from collections import deque
import socket

#UDP_IP = "34.218.77.22" #data center
#UDP_IP = "35.162.126.249"
UDP_IP = "34.208.32.187";
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)

    db = client['cs5412']
    news_data = db['news_data']

    urls = {'CCN': 'https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'bitcoin': 'https://newsapi.org/v2/everything?q=bitcoin&language=en&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'cryptocurrency': 'https://newsapi.org/v2/everything?q=cryptocurrency&language=en&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'blockchain': 'https://newsapi.org/v2/everything?q=blockchain&language=en&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458'}

    recent_news_md5 = deque([])

    while True:
        try:
            print("Updated News")

            for site, url in urls.items():
                res = requests.get(url).json()
                for r in res['articles']:
                    news_md5 = hashlib.md5(r['url'].encode('utf-8')).hexdigest()
                    if news_md5 in recent_news_md5:
                        continue
                    else:
                        if len(recent_news_md5) >= 100:
                            recent_news_md5.popleft()
                        recent_news_md5.append(news_md5)

                    title = r['title']
                    time = dp.parse(r['publishedAt']).strftime('%s')
                    text = r['description']

                    weight = 10
                    source = r['url']

                    news_updated = {'title': title,
                                'time': time,
                                'text': text,
                                'weight': weight,
                                'source': source}

                    sock.sendto(json.dumps(news_updated).encode('utf-8'), (UDP_IP, UDP_PORT))
                    result = news_data.insert_one(news_updated)
                    print(result)
        except:
            print("some thing wrong happens");
        sleep(10)
