__author__ = 'sakhar'


import sys
import urllib2
import urllib
def run(query, target_precision):
    print query
    print target_precision

    precision = 0

    while precision < target_precision:
        relevant = {}
        nonrel = {}

        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+urllib.urlencode({'Query':query})+'%27&$top=10&$format=Atom'
        print bingUrl
        break


if __name__ == "__main__":
    try:
        #query = sys.argv[1]
        #precision = float(sys.argv[2])
        query = 'bill gates'
        precision = 1.0

        if precision > 1 or precision < 0:
            raise Exception()
    except:

        print 'Usage: python main.py <query> <precision>'
        print 'query should be in single quotes and precision a real number between 0 - 1'
        print 'example: python main.py \'bills gates\' 0.6'

    run(query,precision)
