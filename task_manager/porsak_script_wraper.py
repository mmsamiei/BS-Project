import time, threading
import os

os.chdir("../crawlers/porsak/porsak/")
os.system("scrapy crawl porsakSpider")