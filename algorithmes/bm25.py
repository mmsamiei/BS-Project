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
    K1 = 2 
    B = 0.75

    def __init__(self):
        self.client = MongoClient(BM25.mongo_server, BM25.mongo_port)
        self.db = self.client[BM25.mongo_database]
        self.documents_collection = self.db[BM25.documents_collection_name]
        self.iverted_index_collection = self.db[BM25.inverted_index_collections_name]
        self.stop_words = set()
        self.avg_dl = self.get_avg_dl()
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
            temp_scores = self.get_scores(q)
            scores = self.merge_scores(scores, temp_scores)
        print(scores)

    def get_scores(self, word):
        result = {}
        temp = self.iverted_index_collection.find_one({"word":word})
        if temp is not None:    
            documents = temp['documents']
            for document in documents:
                doc_id = document['id']
                freq = document['num'] 
                document_len = 0 #TODO
                avgdl = self.avg_dl
                score = (self.idf(word) * freq *  (BM25.K1 + 1)) / (freq + BM25.K1 * ( 1 - BM25.B + BM25.B * (document_len / avgdl)))
                result[doc_id] = score;
        return result
    
    def idf(self, word):
        N = self.documents_collection.count_documents({})
        temp = self.iverted_index_collection.find_one({"word":word})
        if temp is not None:
            nq = len(temp['documents'])
        else:
            nq = 0
        idf_result = math.log((N-nq+0.5)/(nq+0.5))
        return idf_result

    def merge_scores(self, main_scores, temp_scores):
        result = {}
        for key in main_scores:
            if key in temp_scores:
                result[key] = main_scores[key] + temp_scores[key]
            else:
                result[key] = main_scores[key]
        for key in temp_scores:
            if key not in main_scores:
                result[key] = temp_scores[key]
        return result

    def get_avg_dl(self):
        temp = self.documents_collection.find({})
        total_size = 0
        N = self.documents_collection.count_documents({})
        for document in temp:
            total_size = total_size + len(document['title'].split()) + len (document['body'].split())
        return total_size/N;

    

if __name__ == "__main__":
    bm25 = BM25()
    bm25.search("بچه ععععععععع خوان")
    
