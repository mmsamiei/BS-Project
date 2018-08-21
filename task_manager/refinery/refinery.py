from pymongo import MongoClient
import pprint
import hazm as hazm
import sys
from refinery.mazm import Mazm as mazm
from PersianStemmer import PersianStemmer
import os

class Refinery:
    stop_words = set()
    mongo_server = 'localhost'
    mongo_port = 27017
    mongo_database = 'scraping'
    collections_name = ['porsak','ninisite','applyabroad','javabyab','tebyan']
    #collections_name = ['ninisite']
    destination_collection_name = 'refined'
    
    def __init__(self):
        self.client = MongoClient(Refinery.mongo_server, Refinery.mongo_port)
        self.db = self.client[Refinery.mongo_database]
        self.string = "ss"
        self.stop_words = set()
        os.system("pwd")
        stop_word_file = open("./refinery/PersianStopWordList.txt", "r")
        temp = stop_word_file.read().splitlines() 
        for line in temp:
            self.stop_words.add(line)
        stop_word_file = open("./refinery/StopCharList.txt", "r")
        temp = stop_word_file.read().splitlines() 
        for line in temp:
            self.stop_words.add(line)
        stop_word_file = open("./refinery/NonverbalStopList.txt", "r")
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
            collection.update_one({'_id': post['_id']}, {'$set': {'checked': True}})

    def refine_post(self, post, source_collection):
        new_title = self.refine_text(mazm.my_normalizer(post['title']))
        new_body = self.refine_text(mazm.my_normalizer(post['body']))
        url = post['url']
        refined_post = {"title":new_title, "body": new_body, "url":url, "source": source_collection.name, "checked": False}
        self.insert_post(refined_post)

    def insert_post(self, post):
        refined_posts = self.db[self.destination_collection_name]
        #post_id = refined_posts.insert_one(post).inserted_id
        post_id = refined_posts.update({'url':post['url']},post,upsert = True)
        return post_id

    def refine_text(self, text):
        ps = PersianStemmer()
        lemma = hazm.Lemmatizer()
        new_text = mazm.my_normalizer(text)
        new_text_words = mazm.my_word_tokenizer(new_text)
        text_list = new_text_words
        text_list = [word for word in text_list if word not in self.stop_words]
        #text_list = [mazm.spell_correction(word) for word in new_text_words]
        #text_list = [mazm.my_lemmatizer(word) for word in text_list]
        text_list = [ps.run(word) for word in text_list]
        text_list = [lemma.lemmatize(word) for word in text_list]
        text_list = [word for word in text_list if word not in self.stop_words]
        return (" ".join(text_list))
                
if __name__ == "__main__":
    from mazm import Mazm as mazm
    refinery = Refinery()
    refinery.start()
