import ApplyabroadAutomaticCrawler, NinisiteAutomaticCrawler, AutomaticInvertedIndex, AutomaticRefinement, JavabyabAutomaticCrawler, PorsakAutomaticCrawler, TebyanAutomaticCrawler
import os
import sys
import time 

sys.path.insert(0, "..")

class TaskManager():

    def __init__(self):
        self.apply_abroad_automaticCrawler = ApplyabroadAutomaticCrawler.ApplyabroadAutomaticCrawler(60*60)
        self.ninisite_automatic_crawler = NinisiteAutomaticCrawler.NinisiteAutomaticCrawler(60**60)
        self.javabyab_automatic_crawler = JavabyabAutomaticCrawler.JavabyabAutomaticCrawler(60*60)
        self.porsak_automatic_crawler = PorsakAutomaticCrawler.PorsakAutomaticCrawler(60*60)
        self.tebyan_automatic_crawler = TebyanAutomaticCrawler.TebyanAutomaticCrawler(60*60)
        self.automatic_inverted_index = AutomaticInvertedIndex.AutomaticInvertedIndex(60*60)
        self.automatic_refinement = AutomaticRefinement.AutomaticRefinement(60*60)

    def start(self):
        self.apply_abroad_automaticCrawler.start()
        time.sleep(60)
        self.ninisite_automatic_crawler.start()
        time.sleep(60)
        self.javabyab_automatic_crawler.start()
        time.sleep(60)
        self.porsak_automatic_crawler.start()
        time.sleep(60)
        self.tebyan_automatic_crawler.start()
        time.sleep(60)
        self.automatic_inverted_index.start()
        time.sleep(60)
        self.automatic_refinement.start()
        time.sleep(60)


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.start()
    #time.sleep(120)
    #task_manager.apply_abroad_automaticCrawler.change_interval(10)