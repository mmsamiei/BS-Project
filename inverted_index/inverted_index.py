from pymongo import MongoClient
import pprint
from itertools import groupby

class InvertedIndex():
    mongo_server = 'localhost'
    mongo_port = 27017
    mongo_database = 'scraping'
    source_collections_name = 'refined'
    destination_collection_name = 'invertedIndex'

    def __init__(self):
        self.client = MongoClient(InvertedIndex.mongo_server, InvertedIndex.mongo_port)
        self.db = self.client[InvertedIndex.mongo_database]
        
    
    def start(self):
        source_collection = self.db[InvertedIndex.source_collections_name]
        for post in source_collection.find({"checked": False}):
            self.create_form_post(post)
            source_collection.update_one({'_id': post['_id']}, {'$set': {'checked': True}})
        
    def create_form_post(self, post):
        text = post['title'] + " " + post['body']
        list_of_words = text.split()
        list_of_words.sort()
        groupbyed_list =  [list(group) for key, group in groupby(list_of_words)]
        for word_rep in groupbyed_list:
            self.insert_word(word_rep[0], len(word_rep), post['_id'])

    def insert_word(self, word, number, post_id):
        destination_collection = self.db[InvertedIndex.destination_collection_name]
        result = destination_collection.find_one({"word": word})
        if result is None:
            document = {"word":word , "documents" : [{"id":post_id, "num": number}]}
            destination_collection.insert_one(document)
        else:
            destination_collection.update({'word': word}, {'$push': {'documents': {"id":post_id, "num": number}}})

if __name__ == "__main__":
    inverted_index = InvertedIndex()
    inverted_index.start()