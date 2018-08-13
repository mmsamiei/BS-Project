import time, threading
import os
from MyPeriodic import MyPeriodic
import sys
from refinery.refinery import Refinery as Refinery

class AutomaticRefinement(MyPeriodic):

    def __init__(self, interval):
        MyPeriodic.__init__(self, interval)
        self.refinery = Refinery()
        #os.chdir("../refinery/")
    
    def foo2(self):
        #os.system("python3 refinery.py")
        print("start refinery")
        self.refinery.start()
        print("finish refinery")

if __name__ == "__main__":
    my_refinement = AutomaticRefinement(30)
    my_refinement.start()