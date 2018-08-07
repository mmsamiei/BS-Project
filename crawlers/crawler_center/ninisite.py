import time, threading
import os
from MyPeriodic import MyPeriodic

def foo():
    os.system("scrapy crawl shortTerm")
    print("finish crawl ninisite")

if __name__ == "__main__":
    os.chdir("../ninisite/ninisite/")
    my_thread = MyPeriodic(foo, 60)
    my_thread.start()
    time.sleep(240)
    my_thread.change_interval(120)