import hazm as hazm

class Mazm:
    def my_normalizer(string):
        normalizer = hazm.Normalizer()
        result = normalizer.normalize(string)
        return result
    def my_word_tokenizer(string):
        result = hazm.word_tokenize(string)
        return result
    def my_lemmatizer(string):
        stemmer = hazm.Stemmer()
        lemmatizer = hazm.Lemmatizer()
        current = lemmatizer.lemmatize(string)
        # new = stemmer.stem(current)
        # while(current != new):
        #     current = new
        #     new = stemmer.stem(current)
        # result = new
        if("#" in current): # return bone mozareh!!
            result = current.split("#")[1]
        else:
            result = current
        return result