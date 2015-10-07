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
import sys

accountKey = 'XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
punctuations = list(string.punctuation)
punctuations.append('...')


# Class Document to store each document information
class Document():

    def __init__(self, id, title, des, disp, url):
        self.id = id
        self.title = title
        self.des = des
        self.disp = disp
        self.url = url


def parse_entry(entry):

    """ Parse the xml file returned from Bing
        Return Document object
    """

    # parse the xml file
    content = entry.find('{http://www.w3.org/2005/Atom}content')
    properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
    ID = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ID').text
    Title = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Title').text
    Description = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Description').text
    DisplayUrl = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}DisplayUrl').text
    Url = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Url').text
    return Document(ID, Title, Description, DisplayUrl, Url)


def calc_tf_idf(relevant, nonrel):

    """ Calculates tf_idf values for tokens in relevant
        documents marked by the user

        Inputs: relevant: list of relevant Document objects
                nonrel:   list of non relevant Document objects

        Returns tf_idf:   dictionary of only relevant words
                          word: tf_idf value
    """

    tf = defaultdict(float)
    idf = defaultdict(float)
    list_of_tokens = []

    for doc in relevant.values()+nonrel.values():
        text = doc.title + '\n' + doc.des
        tokens = word_tokenize(text.lower())
        tokens_processed = []

        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        # we compute the number of occurences of the relevant tokens
        for tok in tokens_processed:
            if doc.id in relevant:
                tf[tok] += 1.0
        # we compute the inverted document occurencies for each token
        for tok in set(tokens_processed):
            idf[tok] += 1.0
    N = len(relevant)+len(nonrel)
    tf_idf = {tok: tf[tok]*log(N/idf[tok]) for tok in tf.keys()}

    return tf_idf


def expand_order_query(query, relevant, nonrel):
    """ Expand the query from the previous iteration
        with a single word and order the new query

        Inputs: query of the previous iteration
                relevant documents
                non relevant documents

        Output: A new ordered query
    """


    # call tf-idf, sort the results, select the
    # term with highest tf-idf value
    tf_idf = calc_tf_idf(relevant, nonrel)
    filtered_tf_idf = {tok: tf_idf[tok] for tok in tf_idf
                       if tok not in query}

    sorted_tf_idf = sorted(filtered_tf_idf.items(),
                           key=operator.itemgetter(1),
                           reverse=True)

    new_words = [word[0] for word in sorted_tf_idf[:1] if word[0] not in query]
    # remove duplicates
    seq = query+new_words
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]

    # order the expanded query with respect to the average
    # position of terms first appearance in relevant doc
    positions = {query_term: 0 for query_term in no_dupes}
    for doc in relevant.values():
        text = doc.title + '\n' + doc.des
        tokens = word_tokenize(text.lower())
        c = 0
        seen = set()
        for tok in tokens:
            if tok in no_dupes and tok not in seen:
                seen.add(tok)
                positions[tok] += c
            c += 1
    ordered_no_dupes = sorted(positions.items(),
                              key=operator.itemgetter(1))
    new_query = [word[0] for word in ordered_no_dupes]

    return new_query


def run(query, target_precision):
    """ Iterate until target precision reached
            Call Bing API
            Ask user to mark relevant documents

        Input: initial query
               target precision
    """

    precision = 0.0
    i = 0
    relevant = {}
    nonrel = {}
    while precision < target_precision:
        i += 1
        print '--------------------------------------------'
        print 'Iteration {}'.format(i)
        print 'Query: {}\n'.format(' '.join(query))

        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'\
                  + '+'.join(query) + '%27&$top=10&$format=Atom'
        req = urllib2.Request(bingUrl, headers=headers)
        response = urllib2.urlopen(req)
        root = ET.parse(response)

        if len(root.findall('{http://www.w3.org/2005/Atom}entry')) < 10:
            print 'Number of results < 10'
            break
        precision = 0.0
        # each entry in the xml file under root is a document
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            try:
                doc = parse_entry(entry)
                print 'URL:', doc.url
                print 'Title:', doc.title
                print 'Description:', doc.des

                while True:
                    ans = raw_input("Is this document relevant (y/n) ?\n").lower()
                    if ans == 'y':
                        precision += 1
                        relevant[doc.id] = doc
                        break
                    elif ans == 'n':
                        nonrel[doc.id] = doc
                        break
            except:
                print 'Error with the document!'
                continue

        precision = precision/10.0
        if precision >= target_precision:
            print 'Target precision reached'
            break
        if precision == 0.0:
            print 'No relevant document found'
            break
        query = expand_order_query(query, relevant, nonrel)


if __name__ == "__main__":
    try:
        query = sys.argv[1]
        precision = float(sys.argv[2])
        if precision > 1 or precision < 0:
            raise Exception()
    except:
        print 'Usage: python main.py <query> <precision>'
        print 'query should be in single quotes and precision a real number between 0 - 1'
        print 'example: python main.py \'bills gates\' 0.6'

    run(query.split(' '),precision)
