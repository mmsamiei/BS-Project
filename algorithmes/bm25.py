import sys
sys.path.insert(0, "..")
from refinery.mazm import Mazm as mazm
from pymongo import MongoClient
import math

class BM25:
    mongo_server = 'localhost'
    mongo_port = 27017
    mongo_database = 'scraping'
    inverted_index_collections_name = 'invertedIndex'
    documents_collection_name = 'refined'

    def __init__(self):
        self.client = MongoClient(BM25.mongo_server, BM25.mongo_port)
        self.db = self.client[BM25.mongo_database]
        self.documents_collection = self.db[BM25.documents_collection_name]
        self.iverted_index_collection = self.db[BM25.inverted_index_collections_name]
        self.stop_words = set()
        stop_word_file = open("../refinery/PersianStopWordList.txt", "r")
        temp = stop_word_file.read().splitlines() 
        for line in temp:
            self.stop_words.add(line)

    def search(self, query):
        new_query = mazm.my_normalizer(query)
        new_query_words = mazm.my_word_tokenizer(new_query)
        query_word_list = [mazm.spell_correction(word) for word in new_query_words]
        query_word_list = [mazm.my_lemmatizer(word) for word in query_word_list]
        query_word_list = [word for word in query_word_list if word not in self.stop_words]
        scores = {}
        for q in query_word_list:
            x = self.idf(q)
            print(x)
        print(query_word_list)
        return (" ".join(query_word_list))

    def get_scores(word):
        pass
    
    def idf(self, word):
        N = self.documents_collection.count_documents({})
        temp = self.iverted_index_collection.find_one({"word":word})
        nq = len(temp['documents'])
        idf_result = math.log((N-nq+0.5)/(nq+0.5))
        return idf_result
        
if __name__ == "__main__":
    bm25 = BM25()
    bm25.search("بچه خواه خوان")
    
