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
accountKey = 'XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}


punctuations = list(string.punctuation)
punctuations.append('...')

class Document():
    def __init__(self,id, title, des, disp, url):
        self.id = id
        self.title = title
        self.des = des
        self.disp = disp
        self.url = url

def parse_entry(entry):

    # we parse the xml file
    content = entry.find('{http://www.w3.org/2005/Atom}content')
    properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
    ID = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ID').text
    Title = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Title').text
    Description = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Description').text
    DisplayUrl = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}DisplayUrl').text
    Url = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Url').text

    return Document(ID, Title, Description, DisplayUrl, Url)

def calc_tf_idf(relevant,nonrel):
    tf = defaultdict(int)
    idf = defaultdict(int)


    list_of_tokens = []
    raw_text = []

    for doc in relevant.values()+nonrel.values():
        text = doc.title + '\n' + doc.des
        raw_text.append(text)
        tokens = word_tokenize(text.lower())
        tokens_processed = []

        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        list_of_tokens.append(tokens_processed)

        # we compute the number of occurences of the relevant tokens
        for tok in tokens_processed:
            if doc.id in relevant:
                tf[tok] += 1

        # we compute the inverted document for each token
        for tok in set(tokens_processed):
            idf[tok] += 1
    N = len(relevant)+len(nonrel)

    #tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys() if tok not in query}

    tf_idf = {tok:tf[tok]*log(N/idf[tok]) for tok in tf.keys()}

    return tf_idf

def chi_square(query, relevant,nonrel):
    return



def improve_query(query, relevant,nonrel):

    #chi_square(query, relevant,nonrel)

    tf_idf = calc_tf_idf(relevant,nonrel)
    filtered_tf_idf = {tok:tf_idf[tok] for tok in tf_idf if tok not in query}

    sorted_tf_idf = sorted(filtered_tf_idf.items(), key=operator.itemgetter(1), reverse=True)


    print sorted_tf_idf

    new_words = [word[0] for word in sorted_tf_idf[:2] if word[0] not in query]

    print new_words

    return set(query+new_words)

def run(query, target_precision):


    precision = 0.0
    i = 0
    relevant = {}
    nonrel = {}

    while precision < target_precision:
        i += 0
        print '--------------------------------------------'
        print 'Iteration {}'.format(i)
        print 'Query: {}\n'.format(' '.join(query))

        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+'+'.join(query)+'%27&$top=10&$format=Atom'
        print bingUrl

        req = urllib2.Request(bingUrl, headers = headers)
        response = urllib2.urlopen(req)
        root = ET.parse(response)

        if len(root.findall('{http://www.w3.org/2005/Atom}entry')) < 10:
            print 'Number of results < 10'
            break
        precision = 0.0
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            #ID, Title, Description, DisplayUrl, Url = parse_entry(entry)
            doc = parse_entry(entry)
            print 'Title:', doc.title
            print 'Description:', doc.des
            ans = ''
            while ans not in ['n','y']:
                ans = raw_input("Is this document relevant (y/n) ?\n")
                if ans == 'y':
                    precision += 1
                    relevant[doc.id] = doc
                elif ans == 'n':
                    nonrel[doc.id] = doc

        precision = precision/10.0
        if precision >= target_precision:
            print 'Precision reached'
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
        query = 'jaguar'
        precision = 0.9

        if precision > 1 or precision < 0:
            raise Exception()
    except:

        print 'Usage: python main.py <query> <precision>'
        print 'query should be in single quotes and precision a real number between 0 - 1'
        print 'example: python main.py \'bills gates\' 0.6'

    run(query.split(' '),precision)
