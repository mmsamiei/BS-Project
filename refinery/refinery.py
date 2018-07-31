from pymongo import MongoClient
import pprint
import hazm as hazm
from mazm import Mazm as mazm
class Refinery:
    stop_words = set()
    mongo_server = 'localhost'
    mongo_port = 27017
    mongo_database = 'scraping'
    collections_name = ['test']
    destination_collection_name = 'refined'
    
    def __init__(self):
        self.client = MongoClient(Refinery.mongo_server, Refinery.mongo_port)
        self.db = self.client[Refinery.mongo_database]
        self.string = "ss"
        self.stop_words = set()
        stop_word_file = open("PersianStopWordList.txt", "r")
        temp = stop_word_file.read().splitlines() 
        for line in temp:
            self.stop_words.add(line)
    
    def start(self):
        for collection_name in Refinery.collections_name:
            collection = self.db[str(collection_name)]
            self.refine_collection(collection)
    
    def refine_collection(self, collection):
        for post in collection.find({"checked": False}):
            self.refine_post(post, collection)
    
    def refine_post(self, post, source_collection):
        new_title = self.refine_text(mazm.my_normalizer(post['title']))
        new_body = self.refine_text(mazm.my_normalizer(post['body']))
        url = post['url']
        refined_post = {"title":new_title, "body": new_body, "url":url, "source": source_collection.name, "checked": False}
        self.insert_post(refined_post)

    def insert_post(self, post):
        refined_posts = self.db[self.destination_collection_name]
        post_id = refined_posts.insert_one(post).inserted_id
        return post_id

    def refine_text(self, text):
        new_text = mazm.my_normalizer(text)
        new_text_words = mazm.my_word_tokenizer(new_text)
        text_list = [mazm.spell_correction(word) for word in new_text_words]
        text_list = [mazm.my_lemmatizer(word) for word in text_list]
        text_list = [word for word in text_list if word not in self.stop_words]
        print(text_list)
        return (" ".join(text_list))
                
if __name__ == "__main__":
    refinery = Refinery()
    refinery.start()