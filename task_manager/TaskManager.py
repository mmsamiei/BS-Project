import ApplyabroadAutomaticCrawler, NinisiteAutomaticCrawler, AutomaticInvertedIndex, AutomaticRefinement, JavabyabAutomaticCrawler, PorsakAutomaticCrawler, TebyanAutomaticCrawler
import os
import sys
import time 

sys.path.insert(0, "..")

class TaskManager():

    def __init__(self):
        self.apply_abroad_automaticCrawler = ApplyabroadAutomaticCrawler.ApplyabroadAutomaticCrawler(60*60)
        self.ninisite_automatic_crawler = NinisiteAutomaticCrawler.NinisiteAutomaticCrawler(60*60)
        self.javabyab_automatic_crawler = JavabyabAutomaticCrawler.JavabyabAutomaticCrawler(60*60)
        self.porsak_automatic_crawler = PorsakAutomaticCrawler.PorsakAutomaticCrawler(60*60)
        self.tebyan_automatic_crawler = TebyanAutomaticCrawler.TebyanAutomaticCrawler(60*60)
        self.automatic_inverted_index = AutomaticInvertedIndex.AutomaticInvertedIndex(120)
        self.automatic_refinement = AutomaticRefinement.AutomaticRefinement(60)

    def start(self):
        self.apply_abroad_automaticCrawler.start()
        self.ninisite_automatic_crawler.start()
        #self.javabyab_automatic_crawler.start()
        #self.porsak_automatic_crawler.start()
        #self.tebyan_automatic_crawler.start()
        self.automatic_inverted_index.start()
        self.automatic_refinement.start()

    def turn_off_all(self):
        self.apply_abroad_automaticCrawler.turn_off()
        self.ninisite_automatic_crawler.turn_off()
        #selfjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj.javabyab_automatic_crawler.turn_off()
        #self.porsak_automatic_crawler.turn_off()
        #self.tebyan_automatic_crawler.turn_off()
        self.automatic_inverted_index.turn_off()
        self.automatic_refinement.turn_off()
        self.apply_abroad_automaticCrawler.start()
        print("now turn of all")
    
    def start_all(self):
        self.apply_abroad_automaticCrawler.start()
        self.ninisite_automatic_crawler.start()
        #selfjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj.javabyab_automatic_crawler.turn_off()
        #self.porsak_automatic_crawler.turn_off()
        #self.tebyan_automatic_crawler.turn_off()
        self.automatic_inverted_index.start()
        self.automatic_refinement.start()
        print("now start all")


if __name__ == "__main__":
    task_manager = TaskManager()
    try:
        task_manager.start()
        time.sleep(30)
        task_manager.turn_off_all()
        time.sleep(30)
        task_manager.start_all()
    except KeyboardInterrupt:
        task_manager.turn_off_all()
        sys.exit()