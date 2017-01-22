#!/usr/bin/env python

""" Retrieve information from the autoscout wsdl
"""

import requests

URL = 'http://api.autoscout24.com/AS24_WS_Search'

USERNAME = 'BE_2142129754'
PASSWORD = 'netsarammo2017$'
SELLER_ID = '2142129754'
CULTURE_ID = 'fr-BE'

HEADER = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction': "http://www.autoscout24.com/webapi/IArticleSearch/FindArticles",
    'Content-Length': '577',
    'Host': 'api.autoscout24.com',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)'
}

SOAP = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.autoscout24.com/webapi/" xmlns:data="http://www.autoscout24.com/webapi/data/">
   <soapenv:Header/>
   <soapenv:Body>
      <web:FindArticles>
         <!--Optional:-->
         <web:request>
        <data:culture_id>{culture_id}</data:culture_id>
            <data:vehicle_search_parameters>
               <data:dealer_id>{dealer_id}</data:dealer_id>
            </data:vehicle_search_parameters>
         </web:request>
      </web:FindArticles>
   </soapenv:Body>
</soapenv:Envelope>
"""

def wsdl_query():
    """ Implementation of wsdl query to get data from the server"""


    context = {'dealer_id': SELLER_ID,
               'culture_id': CULTURE_ID,
               'profile_id': USERNAME
              }
    response = requests.post(URL, headers=HEADER, data=SOAP.format(**context), auth=(USERNAME, PASSWORD))
    return response

if __name__ == '__main__':
    wsdl_query()
