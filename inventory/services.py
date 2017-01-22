"""
Module responsible to communicate with the WSDL servers
and handling all the logic of the website.

Note that in order to help me to create the requests I have used the
application: https://www.soapui.org/soap-and-wsdl/working-with-wsdls.html
"""

from datetime import datetime
import xml.etree.ElementTree as ET
import requests

from inventory.models import Brands, Equipments, Color, Fuel, Gear, Painting, Category, Body


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

    def attr_lookup(self, etree, tag):
        """ Extract the value of the tag if it exists

        Input:
            etree :: xml.etree.ElementTree.Element
            tag :: Xpath expression

        Return:
            value :: String
            The value of the Xpath expression or the empty string ""
        """
        value = ""
        item = etree.find(tag, self.name_spaces)
        if item != None:
            value = item.text

        return value

    def vehicles_factory(self, etree_vehicles):
        """ Build a list of vehicules of type Vehicle

        Input:
            etree_vehicles :: [v0 :: xml.etree.ElementTree.Element, ...]

        Returns:
            vehicules :: [v0 :: Vehicule, ...]
        """
        vehicles = list()
        for etree_v in etree_vehicles:
            find = lambda tag: self.attr_lookup(etree_v, tag)
            vehicle = Vehicle()

            vehicle.accident_free = find('a:accident_free')
            vehicle.body_colorgroup_id = find('a:body_colorgroup_id')
            vehicle.body_id = find('a:body_id')
            vehicle.body_painting_id = find('a:body_painting_id')
            vehicle.brand_id = find('a:brand_id')
            vehicle.category_id = find('a:category_id')
            etree_equipment_ids = etree_v.findall('a:equipments/a:equipment_id', self.name_spaces)
            vehicle.equipment_ids = self.equipments_factory(etree_equipment_ids)
            vehicle.fuel_type_id = find('a:fuel_type_id')
            vehicle.gear_type_id = find('a:gear_type_id')
            vehicle.initial_registration_raw = find('a:initial_registration')
            vehicle.kilowatt = find('a:kilowatt')
            vehicle.media_image_feature = find('a:media/a:images/a:image/a:uri')
            vehicle.media_image_count = find('a:media/a:x_code/a:image_count')
            vehicle.mileage = find('a:mileage')
            vehicle.model_id = find('a:model_id')
            vehicle.owners_offer_key = find('a:owners_offer_key')
            vehicle.price = find('a:prices/a:price/a:value')
            vehicle.currency = find('a:prices/a:price/a:currency_id')
            vehicle.vehicle_guid = find('a:vehicle_guid')
            vehicle.vehicle_id = find('a:vehicle_id')
            vehicle.version = find('a:version')
            vehicle.consumption = find('./a:consumption/a:liquid/a:combined')
            vehicle.emiss_class_id = find('./a:emission/a:class_id')
            vehicle.emiss_co2_liquid = find('./a:emission/a:co2_liquid')
            vehicle.avail_begin = find('./a:availability/a:begin')
            vehicle.avail_last_change = find('./a:availability/a:last_change')
            vehicles.append(vehicle)

        return vehicles

    def equipments_factory(self, etree_equipment_ids):
        """ Return a list of equipments

        Input:
            etree_equipment_ids :: [e0 :: xml.etree.ElementTree.Element, ...]
        """
        return [e.text for e in etree_equipment_ids]

class Vehicle(object):
    """ Object storing all the necessary information related to a car"""
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """ """
        self.accident_free = None
        self.body_colorgroup_id = None
        self.body_id = None
        self.body_painting_id = None
        self.brand_id = None
        self.category_id = None
        self.equipment_ids = None
        self.fuel_type_id = None
        self.gear_type_id = None
        self.initial_registration_raw = None
        self.kilowatt = None
        self.media_image_feature = None
        self.media_image_count = None
        self.mileage = None
        self.model_id = None
        self.owners_offer_key = None
        self.price = None
        self.currency = None
        self.vehicle_guid = None
        self.vehicle_id = None
        self.version = None
        self.consumption = None
        self.emiss_class_id = None
        self.emiss_co2_liquid = None
        self.avail_begin = None
        self.avail_last_change = None

    def __str__(self):
        """ Representation of the object"""
        return self.brand_id

    @property
    def brand(self):
        """ Return name of the brand (not the id) """
        return Brands.objects.get(item_id=self.brand_id).description

    @property
    def equipments(self):
        """ Return name of the equipments (not the id) """
        return [Equipments.objects.get(item_id=eid).description for eid in self.equipment_ids]

    @property
    def fuel(self):
        """ Return name of the fuel (not the id) """
        return Fuel.objects.get(item_id=self.fuel_type_id).description

    @property
    def gear(self):
        """ Return name of the fuel (not the id) """
        return Gear.objects.get(item_id=self.gear_type_id).description

    @property
    def color(self):
        """ Return name of the fuel (not the id) """
        return Color.objects.get(item_id=self.body_colorgroup_id).description

    @property
    def body(self):
        """ Return name of the body (not the id) """
        return Body.objects.get(item_id=self.body_id).description

    @property
    def painting(self):
        """ Return name of the painting (not the id) """
        return Painting.objects.get(item_id=self.body_painting_id).description

    @property
    def category(self):
        """ Return name of the body (not the id) """
        return Category.objects.get(item_id=self.category_id).description
    
    @property
    def initial_registration(self):
        return datetime.strptime(self.initial_registration_raw,'%Y-%m-%dT%H:%M:%S').strftime('%m/%y')
