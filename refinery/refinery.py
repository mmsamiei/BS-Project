from pymongo import MongoClient
import pprint
import hazm as hazm

class Refinery:
    mongo_server = 'localhost'
    mongo_port = 27017
    mongo_database = 'scraping'
    collections_name = ['test']
    def __init__(self):
        self.client = MongoClient(Refinery.mongo_server, Refinery.mongo_port)
        self.db = self.client[Refinery.mongo_database]
        self.string = "ss"
    def start(self):
        for collection_name in Refinery.collections_name:
            collection = self.db[str(collection_name)]
            self.refine_collection(collection)
    def refine_collection(self, collection):
        for post in collection.find({"checked": False}):
            self.refine_post(post)
    def refine_post(self, post):
        new_title = self.my_normalizer(post['title'])
        new_body = self.my_normalizer(post['body'])
    def my_normalizer(self, string):
        normalizer = hazm.Normalizer()
        result = normalizer.normalize(string)
        return result
if __name__ == "__main__":
    refinery = Refinery()
    refinery.start()