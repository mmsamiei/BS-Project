import time, threading
import os
import datetime


class MyPeriodic():

    def __init__(self, interval):
        self.interval = interval 
        self.i = 0
    
    def start(self):
        self.t = threading.Timer(1, self.foo)
        self.t.start()
             
    def foo(self):
        global i
        print(datetime.datetime.now())
        self.i = self.i + 1
        self.foo2()
        self.t = threading.Timer(self.interval, self.foo)
        self.t.start()
    
    def change_interval(self, new_interval):
        self.interval = new_interval

    def foo2(self):
        global i
        print("Runned!" + str(i))


if __name__ == "__main__":
    my_thread = MyPeriodic(1)
    my_thread.start()
    time.sleep(6)
    my_thread.change_interval(2)
        
    