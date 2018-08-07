import time, threading
import os
import datetime


class MyPeriodic():

    def __init__(self, foo2, interval):
        self.interval = interval 
        self.foo2 = foo2
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


def my_foo():
    print("1")

if __name__ == "__main__":
    my_thread = MyPeriodic(my_foo, 1)
    my_thread.start()
    time.sleep(6)
    my_thread.change_interval(2)
        
    