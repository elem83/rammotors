"""
Module responsible to communicate with the WSDL servers
and handling all the logic of the website.

Note that in order to help me to create the requests I have used the application:
    https://www.soapui.org/soap-and-wsdl/working-with-wsdls.html
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
    'SOAPAction':\
    "http://www.autoscout24.com/webapi/IArticleSearch/FindArticles",
    'Content-Length': '577',
    'Host': 'api.autoscout24.com',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)'
}

SOAP = """<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:web="http://www.autoscout24.com/webapi/"
    xmlns:data="http://www.autoscout24.com/webapi/data/">
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

def wsdl_findallarticles():
    """ Searching all the articles correspondings to a dealer

    Args:
        url :: String
        The URL endpoint for this request

        username, password :: String
        Credential for accessing the service

        seller_id :: String
        The dealer id for which we request the inventory

        culture_id :: String
        The RFC 1766 culture code

        header :: String
        Expected header expected by the servers

    Returns:
        response :: requests.models.Response
        The response received from the wsdl servers in an object form
        corresponding to Requests module

    Exceptions:
        Timeouts :: requests.exceptions.Timeout
        timeout is not a time limit on the entire response download; rather, an
        exception is raised if the server has not issued a response for timeout
        seconds (more precisely, if no bytes have been received on the
        underlying socket for timeout seconds). If no timeout is specified
        explicitly, requests do not time out.

        ConnectionError, TooManyRedirects :: requests.exceptions.RequestException
        In the event of a network problem (e.g. DNS failure,
        refused connection, etc), Requests will raise a ConnectionError
        exception.
        If a request exceeds the configured number of maximum redirections,
        a TooManyRedirects exception is raised.
    """

    context = {'dealer_id': SELLER_ID,
               'culture_id': CULTURE_ID,
               'profile_id': USERNAME
              }
    response = requests.post(URL, headers=HEADER, data=SOAP.format(**context),
                             auth=(USERNAME, PASSWORD))
    return response

