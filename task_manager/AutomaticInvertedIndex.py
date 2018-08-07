import time, threading
import os
from MyPeriodic import MyPeriodic

class AutomaticInvertedIndex(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        os.chdir("../inverted_index/")
    
    def foo2(self):
        os.system("python3 inverted_index.py")
        print("finish inverted index")

if __name__ == "__main__":
    my_inverted_index = AutomaticInvertedIndex(30)
    my_inverted_index.start()