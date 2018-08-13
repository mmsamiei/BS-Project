import time, threading
import os
from MyPeriodic import MyPeriodic

class JavabyabAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/applyabroad/applyabroad/")
    
    def foo2(self):
        #os.system("scrapy crawl applyabroadSpider")
        print("\t \t \t *** START JAVABYAB")
        os.system("python3 javabyab_script_wraper.py")
        print("finish crawl javabyab")

if __name__ == "__main__":
    my_crawler = JavabyabAutomaticCrawler(30)
    my_crawler.start()