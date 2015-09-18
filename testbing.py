__author__ = 'sakhar'

# this file is used to test Bing API (won't be submitted)

import urllib2
import base64
import xml.etree.ElementTree as ET

'''
bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27gates%27&$top=10&$format=Atom'
#Provide your account key here
accountKey = 'XfbHf/vIn9YQOGFXSYwPnxOOmIWdeM95n39nD5s4FxI'

accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
content = response.read()

#content contains the xml/json response from Bing.
print content
'''
root = ET.parse('x.xml')
print len(root.findall('{http://www.w3.org/2005/Atom}entry'))
for child in root.findall('{http://www.w3.org/2005/Atom}entry'):
    #print child.find('{http://www.w3.org/2005/Atom}id').text
    #print child.find('{http://www.w3.org/2005/Atom}title').text
    content = child.find('{http://www.w3.org/2005/Atom}content')
    properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
    #print properties
    ID = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ID').text
    Title = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Title').text
    Description = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Description').text
    DisplayUrl = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}DisplayUrl').text
    Url = properties.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Url').text
    print 'ID:', ID
    print '\tTitle: ', Title
    print '\tDescription: ', Description
    print '\tDisplayUrl: ', DisplayUrl
    print '\tUrl: ', Url