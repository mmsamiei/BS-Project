import time, threading
import os

os.chdir("../crawlers/applyabroad/applyabroad/")
os.system("scrapy crawl applyabroadSpider")