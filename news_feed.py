import requests
import pprint
import feedparser
import urllib.request
import requests
import dateutil.parser as dp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import hashlib
from time import sleep
from collections import deque

'''
title,
time,
text,
weight,
source
'''

def extract_content_ccn(url):
    driver.get(r['url'])
    news_contents = driver.find_elements_by_css_selector('div.entry-content')
    news = str()
    for i in range(len(news_contents)):
        if news_contents[i].text == 'Advertisement':
            i += 2
        else:
            news += news_contents[i].text
    return news

if __name__ == '__main__':
    # set up the browser driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # start up browser driver
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # start up mongo database
    client = MongoClient('localhost', 27017)

    db = client['cs5412']
    news_data = db['news_data']

    url = ('https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=f462ca2cbbbc445c9c9ed76819a8e458')

    recent_news_md5 = deque([])

    while True:
        res = requests.get(url).json()
        print("Updated News")
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
            text = extract_content_ccn(r['url'])
            weight = 1
            source = r['url']

            news_updated = {'title': title,
                        'time': time,
                        'text': text,
                        'weight': weight,
                        'source': source}
            result = news_data.insert_one(news_updated)
            print(result)
            print()
        sleep(10)
