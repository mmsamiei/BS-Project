import time, threading
import os
from MyPeriodic import MyPeriodic

class NinisiteAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        os.chdir("../ninisite/ninisite/")
    
    def foo2(self):
        os.system("scrapy crawl shortTerm")
        print("finish crawl ninisite")

if __name__ == "__main__":
    my_crawler = NinisiteAutomaticCrawler(20)
    my_crawler.start()