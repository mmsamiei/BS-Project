import time, threading
import os

os.chdir("../crawlers/ninisite/ninisite/")
os.system("scrapy crawl shortTerm")