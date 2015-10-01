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

punctuations = list(string.punctuation)
punctuations.append('...')



X = []
y = []
raw_text = []

query = 'jaguar'
i = 0

values = pickle.load(open('jaguar_'+str(i)))
relevant = values[0]
nonrel = values[1]

for doc in relevant.values()+nonrel.values():
    text = doc.title + '\n' + doc.des
    raw_text.append(text)
    tokens = word_tokenize(text.lower())
    tokens_processed = []

    for tok in tokens:
        if tok not in punctuations:
            tokens_processed.append(tok)
    #print tokens_processed
    X.append( dict(Counter(tokens_processed)))
    if doc.id in relevant:
        y.append(1)
    else:
        y.append(0)

#print X
#print y
vec = DictVectorizer()
#print X
new_X =  vec.fit_transform(X).toarray()
#print vec.get_feature_names()

#bestK = feature_selection.SelectKBest(k=2)
chi2, pval = feature_selection.chi2(new_X,y)

word_tuples = []

for name, c, p in zip(vec.get_feature_names(),chi2,pval):
    word_tuples.append((name, c, p))

sorted_words = sorted(word_tuples, key=operator.itemgetter(1), reverse=True)

for tuple in sorted_words:
    print tuple
#print bestK.fit(new_X,y)
#print DictVectorizer(X)

