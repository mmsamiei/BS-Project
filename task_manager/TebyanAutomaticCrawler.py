import time, threading
import os
from MyPeriodic import MyPeriodic

class TebyanAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/applyabroad/applyabroad/")
    
    def foo2(self):
        #os.system("scrapy crawl applyabroadSpider")
        print("\t \t \t *** START TEBYAN")
        os.system("python3 tebyan_script_wraper.py")
        print("finish crawl TEBYAN")

if __name__ == "__main__":
    my_crawler = TebyanAutomaticCrawler(30)
    my_crawler.start()