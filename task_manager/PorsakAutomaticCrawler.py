import time, threading
import os
from MyPeriodic import MyPeriodic

class PorsakAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/applyabroad/applyabroad/")
    
    def foo2(self):
        #os.system("scrapy crawl applyabroadSpider")
        print("\t \t \t *** START Porsak")
        os.system("python3 porsak_script_wraper.py")
        print("finish crawl porsak")

if __name__ == "__main__":
    my_crawler = PorsakAutomaticCrawler(30)
    my_crawler.start()