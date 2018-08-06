import time, threading
import os
def foo():
    os.system("scrapy crawl shortTerm")
    print("finish crawl ninisite")
    t = threading.Timer(1, foo)
    t.start()

os.chdir("../ninisite/ninisite/")
foo()
