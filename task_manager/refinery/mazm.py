import hazm as hazm
from PersianStemmer import PersianStemmer
import re

class Mazm:

    def my_normalizer(string):
        normalizer = hazm.Normalizer()
        result = normalizer.normalize(string)
        result = self.remove_duplicate_consecutive(result)
        return result

    def remove_duplicate_consecutive(text):
        alphabet = ['ض','ص','ث','ق','ف','غ','ع','ه','خ','ح','ج','چ','ش','س','ی','ب','ل','ا'
        ,'ت','ن','م','ک','گ','ظ','ط','ز','ر','ذ','د','پ','و']
        for char in alphabet:
        reg = char+char+char+'('+char+'*'+')'
        result = re.sub(reg,char, text)
        return result
    
    def my_word_tokenizer(string):
        result = hazm.word_tokenize(string)
        return result

    def spell_correction(word):
        informal_normalizer = hazm.InformalNormalizer()
        corrected_words = informal_normalizer.normalized_word(word)
        return corrected_words[0]
    
    def my_lemmatizer(string):
        ps = PersianStemmer()
        lemmatizer = hazm.Lemmatizer()
        current = ps.run(string)
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