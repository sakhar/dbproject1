'''
Columbia University
COMS E6111 Advanced Database Systems, Fall 2015
Project 1

Students:
Robert Dadashi-Tazehozi, UNI: rd2669
Sakhar Alkhereyf       , UNI: sa3147

'''


import urllib2
import base64
import xml.etree.ElementTree as ET
import string
from nltk.tokenize import *
from math import log
import operator
from collections import defaultdict
from sklearn.feature_selection import chi2
import pickle
#from sklearn.feature_extraction import DictVectorizer
from collections import Counter

accountKey = 'XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}


punctuations = list(string.punctuation)
punctuations.append('...')

# Class Document to store each document information
class Document():
    def __init__(self,id, title, des, disp, url):
        self.id = id
        self.title = title
        self.des = des
        self.disp = disp
        self.url = url

def parse_entry(entry):

    # parse the xml file
    content = entry.find('{http://www.w3.org/2005/Atom}content')
    properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
    ID = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ID').text
    Title = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Title').text
    Description = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Description').text
    DisplayUrl = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}DisplayUrl').text
    Url = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Url').text

    return Document(ID, Title, Description, DisplayUrl, Url)

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



def improve_query(query, relevant,nonrel):

    docs = []
    y = []

    for doc in relevant.values()+nonrel.values():
        bow = {}
        text = doc.title + '\n' + doc.des
        tokens = word_tokenize(text.lower())
        tokens_processed = []

        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        for token in tokens_processed:
            try:
                bow[token]
            except:
                bow[token] = 0
            bow[token] += 1
        docs.append(dict(Counter(tokens_processed)))
        if doc.id in relevant:
            y.append(1)
        else:
            y.append(0)
        docs.append(bow)

        if doc.id in relevant:
            y.append(1)
        else:
            y.append(0)

    '''
    #vec = DictVectorizer()

    #X = vec.fit_transform(docs).toarray()

    #features, pvalue = chi2(X,y)

    word_tuples = []

    for name, c, p in zip(vec.get_feature_names(),features,pvalue):
        word_tuples.append((name, c, p))

    sorted_words = sorted(word_tuples, key=operator.itemgetter(1), reverse=True)

    for tuple in sorted_words:
        print tuple

        #list_of_tokens.append(tokens_processed)

    #chi_square(query, relevant,nonrel)
    '''

    tf_idf = calc_tf_idf(relevant,nonrel)
    filtered_tf_idf = {tok:tf_idf[tok] for tok in tf_idf if tok not in query}

    sorted_tf_idf = sorted(filtered_tf_idf.items(), key=operator.itemgetter(1), reverse=True)

    new_words = [word[0] for word in sorted_tf_idf[:2] if word[0] not in query]

    #print new_words
    for item in sorted_tf_idf:
        print item

    # remove duplicates
    seq = query+new_words
    noDupes = []

    [noDupes.append(i) for i in seq if not noDupes.count(i)]

    return noDupes

def run(query, target_precision):


    precision = 0.0
    i = 0
    relevant = {}
    nonrel = {}

    while precision < target_precision:
        i += 1
        print '--------------------------------------------'
        print 'Iteration {}'.format(i)
        print 'Query: {}\n'.format(' '.join(query))

        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+'+'.join(query)+'%27&$top=10&$format=Atom'
        #print bingUrl

        req = urllib2.Request(bingUrl, headers = headers)
        response = urllib2.urlopen(req)
        root = ET.parse(response)

        if len(root.findall('{http://www.w3.org/2005/Atom}entry')) < 10:
            print 'Number of results < 10'
            break
        precision = 0.0
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            try:

                #ID, Title, Description, DisplayUrl, Url = parse_entry(entry)
                doc = parse_entry(entry)
                print 'URL:', doc.url
                print 'Title:', doc.title
                print 'Description:', doc.des
                ans = ''
                while ans.lower() not in ['n','y']:
                    ans = raw_input("Is this document relevant (y/n) ?\n")
                    if ans == 'y':
                        precision += 1
                        relevant[doc.id] = doc
                    elif ans == 'n':
                        nonrel[doc.id] = doc
            except:
                print 'error with the document!'
                continue

        precision = precision/10.0
        if precision >= target_precision:
            print 'Target precision reached'
            break
        if precision == 0.0:
            print 'No relevant document found'
            break

        # for testing purpose, save all documents after each iteration
        pickle.dump([relevant,nonrel],open(' '.join(query)+'_'+str(i),'w'))
        query = improve_query(query,relevant,nonrel)


if __name__ == "__main__":
    try:
        #query = sys.argv[1]
        #precision = float(sys.argv[2])
        #query = 'taj mahal'
        query = 'musk'
        precision = 0.9

        if precision > 1 or precision < 0:
            raise Exception()
    except:

        print 'Usage: python main.py <query> <precision>'
        print 'query should be in single quotes and precision a real number between 0 - 1'
        print 'example: python main.py \'bills gates\' 0.6'

    run(query.split(' '),precision)
