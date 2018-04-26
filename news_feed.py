#!/usr/bin/python3

import requests
import pprint
import feedparser
import requests
import json
import dateutil.parser as dp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from html.parser import HTMLParser
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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    re = requests.get(url, headers=headers)
    if re is None or re.status_code != 200:
        return None
    #htmlstr = "data:text/html;charset=utf-8," + str(re.content, 'utf-8')
    #driver.get(re.content)
    #print(htmlstr)
    #driver.get(htmlstr)
    driver.get(url)

    #driver.execute_script("document.write('{}')".format(json.dumps(str(re.content, 'utf-8'))))
    '''try:
        news_contents = driver.find_elements_by_css_selector('div.entry-content p')
    except StaleElementReferenceException as e:
        return None
    news = str()
    for i in range(len(news_contents)):
        news_content = str(news_contents[i].text.strip())
        if len(news_content) > 0:
            #print(str(i) + ': ' + news_content)
            news += (news_content + u'\n\n')
    #print(news)'''

    parser = HTMLParser()

    parser.feed(str(re.content, 'utf-8'))

    print(parser)
    return news

if __name__ == '__main__':
    # set up the browser driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }

    # start up browser driver
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=chrome_options, desired_capabilities=d)
    driver.implicitly_wait(15)

    # start up mongo database
    client = MongoClient('localhost', 27017)

    db = client['cs5412']
    news_data = db['news_data']

    urls = {'CCN': 'https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'bitcoin': 'https://newsapi.org/v2/everything?q=bitcoin&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'cryptocurrency': 'https://newsapi.org/v2/everything?q=cryptocurrency&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458',
            'blockchain': 'https://newsapi.org/v2/everything?q=blockchain&sortBy=publishedAt&apiKey=f462ca2cbbbc445c9c9ed76819a8e458'}

    recent_news_md5 = deque([])

    while True:
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
                #if site[:6] == 'Google':
                text = r['description']
                #elif site == 'CCN':
                #    text = extract_content_ccn(r['url'])
                #if text is None:
                #    continue
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
