__author__ = 'sakhar'


import sys
import urllib
import urllib2
import base64
import xml.etree.ElementTree as ET
import string
from nltk.tokenize import *
from math import log
import operator
from collections import defaultdict
from sklearn import feature_selection
import pickle
from sklearn.feature_extraction import DictVectorizer
#from sklearn.feature_extraction.text import
from main import Document
from collections import Counter
from bs4 import BeautifulSoup


punctuations = list(string.punctuation)
punctuations.append('...')

def calc_tf_idf(relevant,nonrel):
    tf = defaultdict(float)
    idf = defaultdict(float)


    list_of_tokens = []
    #raw_text = []

    for doc in relevant.values()+nonrel.values():
        text = doc.title + '\n' + doc.des
        #raw_text.append(text)
        tokens = word_tokenize(text.lower())
        tokens_processed = []

        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        list_of_tokens.append(tokens_processed)

        # we compute the number of occurences of the relevant tokens
        for tok in tokens_processed:
            if doc.id in relevant:
                tf[tok] += 1.0

        # we compute the inverted document for each token
        for tok in set(tokens_processed):
            idf[tok] += 1.0
    N = len(relevant)+len(nonrel)

    #tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys() if tok not in query}

    tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys()}

    return tf_idf

def calc_tf_idf(relevant,nonrel):
    tf = defaultdict(float)
    idf = defaultdict(float)


    list_of_tokens = []
    #raw_text = []

    for doc in relevant.values()+nonrel.values():
        text = doc.title + '\n' + doc.des
        #raw_text.append(text)
        tokens = word_tokenize(text.lower())
        tokens_processed = []

        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        list_of_tokens.append(tokens_processed)

        # we compute the number of occurences of the relevant tokens
        for tok in tokens_processed:
            if doc.id in relevant:
                tf[tok] += 1.0

        # we compute the inverted document for each token
        for tok in set(tokens_processed):
            idf[tok] += 1.0
    N = len(relevant)+len(nonrel)

    #tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys() if tok not in query}

    tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys()}

    return tf_idf


#X = []
#y = []
raw_text = []

query = 'musk'
i = 1

values = pickle.load(open(query+'_'+str(i)))
relevant = values[0]
nonrel = values[1]

#print X
#print y
#vec = DictVectorizer()
#print X
#new_X =  vec.fit_transform(X).toarray()
#print vec.get_feature_names()

#bestK = feature_selection.SelectKBest(k=2)
#chi2, pval = feature_selection.chi2(new_X,y)

word_tuples = []

'''for name, c, p in zip(vec.get_feature_names(),chi2,pval):
    word_tuples.append((name, c, p))
'''

#for tuple in sorted_words:
#    print tuple
#print bestK.fit(new_X,y)
#print DictVectorizer(X)

tf_idf = calc_tf_idf(relevant,nonrel)
filtered_tf_idf = {tok:tf_idf[tok] for tok in tf_idf if tok not in query}

sorted_tf_idf = sorted(filtered_tf_idf.items(), key=operator.itemgetter(1), reverse=True)

print sorted_tf_idf