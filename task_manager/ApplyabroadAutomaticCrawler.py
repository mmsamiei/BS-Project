import time, threading
import os
from MyPeriodic import MyPeriodic

class ApplyabroadAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/applyabroad/applyabroad/")
    
    def foo2(self):
        #os.system("scrapy crawl applyabroadSpider")
        print("\t \t \t *** START APPLYABROAD")
        os.system("python3 applyabroad_script_wraper.py")
        print("finish crawl applyabroad")

if __name__ == "__main__":
    my_crawler = ApplyabroadAutomaticCrawler(30)
    my_crawler.start()