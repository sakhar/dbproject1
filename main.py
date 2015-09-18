__author__ = 'sakhar'


import sys
def run(query, target_precision):
    print query
    print target_precision


if __name__ == "__main__":
    try:
        query = sys.argv[1]
        precision = float(sys.argv[2])
        run(query,precision)
    except:
        print 'Usage: python main.py <query> <precision>'
        print 'query should be in single quotes and precision a real number between 0 - 1'
        print 'example: python main.py \'bills gates\' 0.6'
