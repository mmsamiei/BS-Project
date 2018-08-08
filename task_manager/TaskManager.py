import ApplyabroadAutomaticCrawler, NinisiteAutomaticCrawler, AutomaticInvertedIndex, AutomaticRefinement
import os
import sys
import time 

sys.path.insert(0, "..")

class TaskManager():

    def __init__(self):
        self.apply_abroad_automaticCrawler = ApplyabroadAutomaticCrawler.ApplyabroadAutomaticCrawler(60)
        self.ninisite_automatic_crawler = NinisiteAutomaticCrawler.NinisiteAutomaticCrawler(60)
        self.automatic_inverted_index = AutomaticInvertedIndex.AutomaticInvertedIndex(5*60)
        self.automatic_refinement = AutomaticRefinement.AutomaticRefinement(5*60)

    def start(self):
        self.apply_abroad_automaticCrawler.start()
        self.ninisite_automatic_crawler.start()
        self.automatic_inverted_index.start()
        self.automatic_refinement.start()


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.start()
    time.sleep(120)
    task_manager.apply_abroad_automaticCrawler.change_interval(10)