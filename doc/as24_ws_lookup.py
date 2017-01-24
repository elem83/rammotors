#!/usr/bin/env python

""" Retrieve lookup value from Autocout24 """

import xml.dom.minidom
import requests


URL = 'http://api.autoscout24.com/AS24_WS_Lookup'

USERNAME = 'BE_2142129754'
PASSWORD = 'netsarammo2017$'
SELLER_ID = '2142129754'

HEADER = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction': "http://www.autoscout24.com/webapi/ILookup/GetLookupData",
    'Content-Length': '433',
    'Host': 'api.autoscout24.com',
    'Connection': 'Keep-Alive',
    'User-Agent':  'Apache-HttpClient/4.1.1 (java 1.5)'
}

SOAP = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.autoscout24.com/webapi/" xmlns:data="http://www.autoscout24.com/webapi/data/">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetLookupData>
         <!--Optional:-->
         <web:request>
            <data:culture_id>{culture_id}</data:culture_id>
         </web:request>
      </web:GetLookupData>
   </soapenv:Body>
</soapenv:Envelope>
"""

def lookup(culture_id='fr-BE'):
    """ Retrieve lookup key/value from Autoscout24 """
    context = {'culture_id': culture_id}
    soap_request = SOAP.format(**context)
    response = requests.post(URL, headers=HEADER, data=soap_request,\
                             auth=(USERNAME, PASSWORD))
    response = xml.dom.minidom.parseString(response.content)
    return response.toprettyxml()

if __name__ == '__main__':
    print(lookup())
