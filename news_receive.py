import socket
import json
from pymongo import MongoClient
from datetime import datetime

UDP_IP = "0.0.0.0"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


client = MongoClient('localhost', 27017)

db = client['cs5412']
news_data = db['news_data']


while True:
    try:
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        news_updated = json.loads(data.decode("utf-8"))
        #print(news_updated)
        result = news_data.insert_one(news_updated)
        #ts = datetime.datetime.time(datetime.datetime.now())
        #news_data.remove({time: {'$lt': ts - 250}})
    except:
        print("This is an error message!")
