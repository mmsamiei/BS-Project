import time, threading
import os

os.chdir("../crawlers/javabyab/javabyab/")
os.system("scrapy crawl javabyabSpider")