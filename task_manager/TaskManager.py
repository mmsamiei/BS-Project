import ApplyabroadAutomaticCrawler, NinisiteAutomaticCrawler, AutomaticInvertedIndex, AutomaticRefinement, JavabyabAutomaticCrawler, PorsakAutomaticCrawler, TebyanAutomaticCrawler
import os
import sys
import time 

sys.path.insert(0, "..")

class TaskManager():

    def __init__(self):
        self.lock = False
        self.apply_abroad_automaticCrawler = ApplyabroadAutomaticCrawler.ApplyabroadAutomaticCrawler(2*60*60)
        self.ninisite_automatic_crawler = NinisiteAutomaticCrawler.NinisiteAutomaticCrawler(60*60)
        self.javabyab_automatic_crawler = JavabyabAutomaticCrawler.JavabyabAutomaticCrawler(3*60*60)
        self.porsak_automatic_crawler = PorsakAutomaticCrawler.PorsakAutomaticCrawler(4*60*60)
        self.tebyan_automatic_crawler = TebyanAutomaticCrawler.TebyanAutomaticCrawler(3*60*60)
        self.automatic_inverted_index = AutomaticInvertedIndex.AutomaticInvertedIndex(300)
        self.automatic_refinement = AutomaticRefinement.AutomaticRefinement(30)

    def turn_off_all(self):
        self.apply_abroad_automaticCrawler.turn_off()
        self.ninisite_automatic_crawler.turn_off()
        self.javabyab_automatic_crawler.turn_off()
        self.porsak_automatic_crawler.turn_off()
        self.tebyan_automatic_crawler.turn_off()
        self.automatic_inverted_index.turn_off()
        self.automatic_refinement.turn_off()
        print("now turn of all")
    
    def start_all(self):
        self.apply_abroad_automaticCrawler.start()
        self.ninisite_automatic_crawler.start()
        self.javabyab_automatic_crawler.start()
        self.porsak_automatic_crawler.start()
        self.tebyan_automatic_crawler.start()
        self.automatic_inverted_index.start()
        self.automatic_refinement.start()
        print("now start all")


if __name__ == "__main__":
    task_manager = TaskManager()
    con = True
    try:
        while(con):
            while(task_manager.lock == True):
                continue
            command = input("your command:\n")
            if command == '1':
                task_manager.start_all()   
            if command == '2':
                task_manager.turn_off_all()
            if command == '3':
                task_manager.turn_off_all()
                con = False
                sys.exit()
            if command == '4':
                scraper_number = input("scraper number:\n")
                if(scraper_number == '0'):
                    period = input("period to hour:\n")
                    task_manager.apply_abroad_automaticCrawler.change_interval(period*3600)
                if(scraper_number == '1'):
                    print("ninisite")
                    period = input("period to hour:\n")
                    task_manager.ninisite_automatic_crawler.change_interval(period*3600)
                if(scraper_number == '2'):
                    print("javabyab")
                    period = input("period to hour:\n")
                    task_manager.javabyab_automatic_crawler.change_interval(period*3600)
                if(scraper_number == '3'):
                    print("porsak")
                    period = input("period to hour:\n")
                    task_manager.porsak_automatic_crawler.change_interval(period*3600) 
                if(scraper_number == '4'):
                    print("javabyab")
                    period = input("period to hour:\n")
                    task_manager.tebyan_automatic_crawler.change_interval(period*3600) 
    except SystemExit:
        print("sys.exit() worked as expected")
    except KeyboardInterrupt:
        task_manager.turn_off_all()
        sys.exit()
    except Exception as error:
        raise Exception('general exceptions not caught by specific handling')
