import time, threading
import os

os.chdir("../crawlers/tebyan/tebyan/")
os.system("scrapy crawl tebyanSpider")