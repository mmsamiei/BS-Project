import time, threading
import os
from MyPeriodic import MyPeriodic

class NinisiteAutomaticCrawler(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        #os.chdir("../crawlers/ninisite/ninisite/")
    
    def foo2(self):
        #os.system("scrapy crawl shortTerm")
        print("\t \t \t *** NINISITE")
        os.system("python3 ninisite_script_wraper.py")
        print("finish crawl ninisite")

if __name__ == "__main__":
    my_crawler = NinisiteAutomaticCrawler(30)
    my_crawler.start()