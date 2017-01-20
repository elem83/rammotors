"""
Module responsible to communicate with the WSDL servers
and handling all the logic of the website.

Note that in order to help me to create the requests I have used the
application: https://www.soapui.org/soap-and-wsdl/working-with-wsdls.html
"""


import xml.etree.ElementTree as ET
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


class WsdlAutoscout24(object):
    """ This object keep track of one request/response from Autoscout"""

    def __init__(self):
        self.response = self.wsdl_find_articles()

    @property
    def name_spaces(self):
        """ Return the name spaces that will be used during the XPath """

        name_spaces = {'s':'http://schemas.xmlsoap.org/soap/envelope/',
                       'default': 'http://www.autoscout24.com/webapi/',
                       'a': 'http://www.autoscout24.com/webapi/data/'
                      }

        return name_spaces

    def uri_images(self, size):
        """ Return the base URI for the images

        Input:
            size :: [big|main|small|thumbnails] :: String

        Return:
            uri :: String
        """
        if size == 'big':
            return 'http://pic.autoscout24.net/images-big/'
        elif size == 'main':
            return 'http://pic.autoscout24.net/images/'
        elif size == 'small':
            return 'http://pic.autoscout24.net/images-small/'
        elif size == 'thumbnails':
            return 'http://pic.autoscout24.net/thumbnails-big/'
        else:
            raise ValueError('Not a correct size parameter')

    def wsdl_find_articles(self):
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
            Nothing

        Set Instance Variable:
            self.response :: requests.models.Response
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

        context = {'dealer_id': SELLER_ID, 'culture_id': CULTURE_ID,
                   'profile_id': USERNAME}
        response = requests.post(URL, headers=HEADER,
                                 data=SOAP.format(**context),
                                 auth=(USERNAME, PASSWORD))
        return response

    def __call__(self):
        """ Function that will be used to build a list of vehicle
        Input:

        Return:
            vehicules :: [v1 :: Vehicle, v2 :: Vehicle, ...]
        """
        etree_vehicles = self.etree_vehicles()
        vehicles = self.vehicles_factory(etree_vehicles)
        return vehicles

    def etree_vehicles(self):
        """ Extract the list of vehicle in etree format """

        root = ET.fromstring(self.response.content)
        etree_vehicles = root.findall(".//a:vehicle", self.name_spaces)
        return etree_vehicles

    def vehicles_factory(self, etree_vehicles):
        """ Build a list of vehicules of type Vehicle

        Input:
            etree_vehicles :: [v0 :: xml.etree.ElementTree.Element, ...]

        Returns:
            vehicules :: [v0 :: Vehicule, ...]
        """
        name_spaces = self.name_spaces
        vehicles = list()
        for etree_v in etree_vehicles:
            vehicle = Vehicle()
            vehicle.brand_id = etree_v.find('a:brand_id', name_spaces).text
            vehicle.model_id = etree_v.find('a:model_id', name_spaces).text
            vehicle.mileage = etree_v.find('a:mileage', name_spaces).text
            vehicle.price = etree_v.find('.//a:value', name_spaces).text
            vehicle.uri_image_feature = \
                    etree_v.find('.//a:uri', name_spaces).text
            vehicles.append(vehicle)

        return vehicles


class Vehicle(object):
    """ Object storing all the necessary information related to a car"""

    def __init__(self):
        """ """
        self.brand_id = None
        self.model_id = None
        self.mileage = None
        self.price = None
        self.currency = 'EUR'
        self.uri_image_feature = None

    def __str__(self):
        """ Representation of the object"""
        return self.brand_id
