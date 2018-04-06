from __future__ import unicode_literals
import os
import re
import sys
import time
import pytz
import datetime
import hashlib
from pathlib import Path
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import requests
from pymongo import MongoClient
from pprint import pprint


sites = [
    {
        'name': 'jinsecaijing',
        'chinese_name': '金色财经',
        'url': 'http://www.jinse.com/lives',
        'date_pattern': r"(\d{4})\.(\d{2})\.(\d{1,2})(.+)",
        'time': 'p.live-time',
        'news_list': 'div.con-item.clearfix.lost-area',
        'content': 'div.live-info'
    },
    {
        'name': 'bishijie',
        'chinese_name': '币世界',
        'url': 'http://www.bishijie.com/kuaixun/',
        'news_list': 'div.kuaixun_list',
        'date_pattern': r"(今天|昨天)(.*)(\d{2})月(\d{1,2})日(.*)"
    }
]

webhook_url = 'https://hooks.slack.com/services/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'

news_hash = {}
news_id = 0
new_count_limit = 1000
tz = pytz.timezone('Asia/Shanghai')

def clear_old_news_hash(number):
    global news_hash
    to_del = [k for k in sorted(news_hash, key=news_hash.get, reverse=False)]
    #print('Before clearing')
    #print(news_hash)

    num_clear = 0
    for k in to_del:
        del news_hash[k]
        num_clear += 1
        if num_clear == number:
            break

    #print('After clearing')
    #print(news_hash)

def print_time(year, month, day, hour, minute):
    print(year + '-' + month + '-' + day + ' ' + hour + ':' + minute)

def date_to_timestamp(year, month, day):
    return int(time.mktime(datetime.date(int(year),int(month),int(day)).timetuple()))

def get_hour_and_minutes(news_time):
    return news_time.split(':')

def is_time_format(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
def generate_id(s):
    return str(hash(s) % ((sys.maxsize + 1) * 2))

def extract_content_jinsecaijing(site):
    elements = driver.find_elements_by_css_selector(site['news_list'])

    flattened_texts = str()

    for element in elements:
        flattened_texts += element.text

    texts = []
    for text in flattened_texts.split('\n'):
        if len(text) > 0:
            if re.match(site['date_pattern'], text) is not None:
                year_month_day = text.split('.')
                year = year_month_day[0]
                month = year_month_day[1]
                day = year_month_day[2][:2]
                unix_time = date_to_timestamp(year, month, day)

            elif is_time_format(text[:4]):
                content = text[5:]
                [hour, minute] = get_hour_and_minutes(text[:5])
                #print_time(year, month, day, hour, minute)
                hour = int(hour)
                minute = int(minute)
                time_stamp = unix_time + hour * 3600 + minute * 60

            elif text[:2] == '利空':
                news_full_content = content.split('】')
                if len(news_full_content) == 1:
                    news_title = ''
                    news_content = news_full_content[0]
                else:
                    news_title = news_full_content[0][1:]
                    news_content = news_full_content[1]

                fall = text[3:]

            elif text[:2] == '利好':
                rise = text[3:]

                hc = generate_id(news_content)

                if hc in news_hash:
                    continue
                else:
                    news_hash[hc] = time_stamp

                news_data = {
                                'id': hc,
                                'site': site['name'],
                                'time': time_stamp,
                                'title': news_title,
                                'summary': '',
                                'text_content': news_content,
                                'fig_content': [],
                                'link': '',
                                'keywords': [],
                                'rise': rise,
                                'fall': fall
                            }
                print(news_data)

                news_collection.news.insert_one(news_data)
            else:
                content += text


def extract_content_bishijie(site):
    elements = driver.find_elements_by_css_selector(site['news_list'])
    now = datetime.datetime.now(tz)
    year = now.strftime("%Y")
    texts = str()

    for element in elements:
        texts += element.text

    for text in texts.split('\n'):
        if len(text) > 0:
            if re.match(site['date_pattern'], text) is not None:
                month_day = re.match(site['date_pattern'], text).group(3,4)
                month = month_day[0]
                day = month_day[1]
                unix_time = date_to_timestamp(year, month, day)

            elif is_time_format(text):
                [hour, minute] = get_hour_and_minutes(text)
                #print_time(year, month, day, hour, minute)
                hour = int(hour) + 13
                if hour >= 24:
                    hour -= 24
                minute = int(minute)

                time_stamp = unix_time + hour * 3600 + minute * 60

            elif text[0] == '【':
                news_full_content = text.split('】')
                if len(news_full_content) == 1:
                    news_title = ''
                    news_content = news_full_content[0]
                else:
                    news_title = news_full_content[0][1:]
                    news_content = news_full_content[1]

                #global news_id
                #news_id += 1

                hc = generate_id(news_content)

                if hc in news_hash:
                    continue
                else:
                    news_hash[hc] = time_stamp

                news_data = {
                                'id': hc,
                                'site': site['name'],
                                'time': time_stamp,
                                'title': news_title,
                                'summary': '',
                                'text_content': news_content,
                                'fig_content': [],
                                'link': '',
                                'keywords': [],
                                'rise': '',
                                'fall': ''
                            }

                news_collection.news.insert_one(news_data)
                print(news_data)


def extract_content_with_format(site):
    driver.get(site['url'])
    time.sleep(15)
    if site['name'] == 'jinsecaijing':
        extract_content_jinsecaijing(site)
    elif site['name'] == 'bishijie':
        extract_content_bishijie(site)
    '''
    global news_id
    id_log_file = Path("./id_log")
    if id_log_file.is_file():
        with open(id_log_file, 'w') as f:
            f.write(str(news_id))
    '''


if __name__ == '__main__':
    # set up the browser driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # start up browser driver
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # start up mongo database
    db_client = MongoClient()

    news_collection = db_client['news_data']

    # retrieve id data
    '''id_log_file = Path("./id_log")
    if id_log_file.is_file():
        with open(id_log_file, 'r') as f:
            id_start = f.readline()
            news_id = int(id_start) + 1
            f.close()
    else:
        with open(id_log_file, 'w') as f:
            news_id = 0
            f.write('0')
            f.close()'''
    last_updated = news_collection.news.find().sort("time", -1).limit(100)
    for r in last_updated:
        news_hash[r['id']] = r['time']

    while True:
        for site in sites:
            if len(news_hash) >= new_count_limit:
                clear_old_news_hash(new_count_limit / 10)

            print(str(datetime.datetime.now()) + ' Latest news from ' + site['chinese_name'])

            extract_content_with_format(site)

            time.sleep(10)

    #for news in news_collection.news.find():
        #pprint(news)
    driver.quit()
