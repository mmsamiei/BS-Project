import time, threading
import datetime
import os
from MyPeriodic import MyPeriodic

class Test(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/applyabroad/applyabroad/")
    
    def foo2(self):
        #os.system("scrapy crawl applyabroadSpider")
        print(datetime.datetime.now())

if __name__ == "__main__":
    my_crawler = Test(1)
    my_crawler.start()
    time.sleep(10)
    my_crawler.turn_off()
    time.sleep(10)
    my_crawler.start()
    time.sleep(10)
    my_crawler.change_interval(2)