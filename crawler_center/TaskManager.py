import ApplyabroadAutomaticCrawler, NinisiteAutomaticCrawler, AutomaticInvertedIndex, AutomaticRefinement

class TaskManager():

    def __init__(self):
        self.apply_abroad_automaticCrawler = ApplyabroadAutomaticCrawler(60)
        self.ninisite_automatic_crawler = NinisiteAutomaticCrawler(60)
        self.automatic_inverted_index = AutomaticInvertedIndex(5*60)
        self.automatic_refinement = AutomaticRefinement(5*60)

    def start(self)
        apply_abroad_automaticCrawler.start()
        ninisite_automatic_crawler.start()
        automatic_inverted_index.start()
        automatic_refinement.start()

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.start()