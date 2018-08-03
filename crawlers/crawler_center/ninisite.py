import time, threading
import os
def foo():
    os.system("scrapy crawl shortTerm")
    print("finish crawl ninisite")
    threading.Timer(1, foo).start()

os.chdir("../ninisite/ninisite/")
foo()
