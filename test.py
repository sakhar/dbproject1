# usage python test.py

import base64
import xml.etree.ElementTree as ET
import sys
from nltk.tokenize import *
import string 
from collections import defaultdict
from math import log
import operator
import urllib2

query = 'jaguar'
precision = 0.9

# we limit the number of iterations to 10
for i in range(10):
    print '--------------------------------------------'
    print 'Iteration {}'.format(i)
    print 'Query: {}\n'.format(query)
    
    # compute Bing query
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+query+'%27&$top=10&$format=Atom'
    accountKey = 'XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    root = ET.parse(response)
    if len(root.findall('{http://www.w3.org/2005/Atom}entry')) < 10:
        print 'Number of results < 10'
        break
    
    # we initialize the data structures
    list_of_tokens = []
    raw_text = []
    count_relevance = 0
    tf = defaultdict(int)
    idf = defaultdict(int)

    for child in root.findall('{http://www.w3.org/2005/Atom}entry'):
        
        # we parse the xml file
        content = child.find('{http://www.w3.org/2005/Atom}content')
        properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
        ID = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ID').text
        Title = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Title').text
        Description = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Description').text
        DisplayUrl = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}DisplayUrl').text
        Url = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Url').text

        # For each URL title and description, we create a list of tokens
        text = Title + '\n' + Description
        raw_text.append(text)
        tokens = word_tokenize(text.lower())
        tokens_processed = []
        punctuations = list(string.punctuation)
        punctuations.append('...')
        for tok in tokens:
            if tok not in punctuations:
                tokens_processed.append(tok)
        list_of_tokens.append(tokens_processed)

        # We now ask the user if the web page is relevant or not,
        # we compute the number of occurences of the relevant tokens
        relevant = ''
        print(text)
        while relevant not in ['n','y']:
            relevant = raw_input("Is this document relevant (y/n) ?\n")
            if relevant == 'y':
                count_relevance += 1
                for tok in tokens_processed:
                    tf[tok] += 1

        # we compute the inverted document for each token
        for tok in set(tokens_processed):
            idf[tok] += 1

    if count_relevance/10 >= precision:
        print 'Precision reached'
        break

    if count_relevance == 0:
        print 'No relevant document found'
        break

    # we selected the new query term for the query having the largest tf-idf
    tf_idf = {tok:tf[tok]*log(10/idf[tok]) for tok in tf.keys() if tok not in query}
    max_tf_idf = 0
    for key in tf_idf:
        if tf_idf[key] > max_tf_idf:
            new_term = key
            max_tf_idf = tf_idf[key]

    query += '+'+new_term