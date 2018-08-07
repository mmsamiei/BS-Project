import time, threading
import os
import datetime
i = 0 

class MyThread():

    def __init__(self, foo2):
        self.interval = 1
        self.foo2 = foo2
    
    def start(self):
        self.t = threading.Timer(1, self.foo)
        self.t.start()
             
    def foo(self):
        global i
        print(datetime.datetime.now())
        i = i + 1
        self.t = threading.Timer(self.interval, self.foo)
        self.t.start()
    

    def change_interval(self, new_interval):
        self.interval = new_interval


def my_foo():
    print("1")

if __name__ == "__main__":
    my_thread = MyThread(my_foo)
    my_thread.start()
        
    