import time, threading
import os
def foo():
    os.system("scrapy crawl applyabroadSpider")
    print("finish crawl ninisite")
    threading.Timer(60, foo).start()

os.chdir("../applyabroad/applyabroad/")
foo()