# pylint: disable=fixme, cell-var-from-loop, no-self-use, too-many-public-methods
"""
Module responsible to communicate with the WSDL servers
and handling all the logic of the website.

Note that in order to help me to create the requests I have used the
application: https://www.soapui.org/soap-and-wsdl/working-with-wsdls.html
"""
from collections import defaultdict

from datetime import datetime
import xml.etree.ElementTree as ET
import requests

from inventory.models import Enumeration


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

HEADER_VEHICLE_DETAILS = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction':\
        "http://www.autoscout24.com/webapi/IArticleSearch/GetArticleDetails",
    'Content-Length': '498',
    'Host': 'api.autoscout24.com',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)'
}

SOAP_VEHICLE_DETAILS = """<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:web="http://www.autoscout24.com/webapi/"
    xmlns:data="http://www.autoscout24.com/webapi/data/">
    <soapenv:Header/>
    <soapenv:Body>
        <web:GetArticleDetails>
            <!--Optional:-->
            <web:request>
                <data:culture_id>{culture_id}</data:culture_id>
                <data:vehicle_id>{vehicle_id}</data:vehicle_id>
            </web:request>
        </web:GetArticleDetails>
    </soapenv:Body>
</soapenv:Envelope>
"""

URL_LOOKUP = 'http://api.autoscout24.com/AS24_WS_Lookup'

HEADER_LOOKUP = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction': "http://www.autoscout24.com/webapi/ILookup/GetLookupData",
    'Content-Length': '433',
    'Host': 'api.autoscout24.com',
    'Connection': 'Keep-Alive',
    'User-Agent':  'Apache-HttpClient/4.1.1 (java 1.5)'
}

SOAP_LOOKUP = """
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
    soap_request = SOAP_LOOKUP.format(**context)
    response = requests.post(URL_LOOKUP, headers=HEADER_LOOKUP, \
                                data=soap_request,\
                            auth=(USERNAME, PASSWORD))
    return response

def get_article_details(vehicle_id):
    """
    Implementation of the GetArticleDetails from WSDL Autoscout24
    """
    context = {'culture_id': CULTURE_ID, 'vehicle_id': vehicle_id}
    response = requests.post(URL, headers=HEADER_VEHICLE_DETAILS,\
                                data=SOAP_VEHICLE_DETAILS.format(**context),\
                                auth=(USERNAME, PASSWORD))
    return response

def find_articles():
    """
    Implementation of the find_articles from WSDL Autoscout24
    """
    context = {'dealer_id': SELLER_ID, 'culture_id': CULTURE_ID}
    response = requests.post(URL, headers=HEADER,\
                                data=SOAP.format(**context),\
                                auth=(USERNAME, PASSWORD))
    return response

class AS24WSSearch(object):
    """ Implementation of the WSDL API of Autoscout24 """

    #TODO: Check if not better to create an attribute
    @property
    def name_spaces(self):
        """ Return the name spaces that will be used during the XPath """

        name_spaces = {'s':'http://schemas.xmlsoap.org/soap/envelope/',
                       'default': 'http://www.autoscout24.com/webapi/',
                       'a': 'http://www.autoscout24.com/webapi/data/'
                      }

        return name_spaces

    def list_vehicles(self):
        """ Implementation of FindArticles

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
            vehicles :: [Vehicle, ... ]

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
        etree_vehicles = self._etree_vehicles(find_articles().content)
        vehicles = self._vehicles_factory(etree_vehicles)
        return vehicles

    def details_vehicle(self, vehicle_id):
        """ Return details of a vehicle

        Input:
            vehicle_id :: Numeric value (String)

        Return:
            vehicle :: Vehicle

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
        etree_vehicles = self._etree_vehicles(\
                            get_article_details(vehicle_id).content)
        vehicle = self._vehicle_factory(etree_vehicles[0])
        return vehicle

    def get_lookup_data(self):
        """ Implementation of GetLookupData

        Return:
            enum :: [{'name': name, 'item_id': item_id, 'text': item_text},...]
            """

        return [self._get_elem(elem) for elem in self._parse_xml(lookup().content)]

    def _parse_xml(self, soap_response):
        """ Parse the XML received from the lookup

        Input:
            soap_response :: String

        Return:
            elements :: [xml.etree.ElementTree, ...]
        """
        root = ET.fromstring(soap_response)
        elements = root.find('.//a:elements', self.name_spaces)
        return elements

    def _get_elem(self, element):
        """ Helper to fill retrieve all element from the enumeration.xml """
        name = element.find('a:name', self.name_spaces).text
        item_id = element.find('a:id', self.name_spaces).text
        item_text = element.find('a:text', self.name_spaces).text
        return {'name': name, 'item_id': item_id, 'text': item_text}

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
        elif size == 'thumb':
            return 'http://pic.autoscout24.net/thumbnails-big/'
        else:
            raise ValueError('Not a correct size parameter')

    def _etree_vehicles(self, response):
        """ Extract the list of vehicle in etree format """

        root = ET.fromstring(response)
        etree_vehicles = root.findall(".//a:vehicle", self.name_spaces)
        return etree_vehicles

    def _vehicle_factory(self, etree_vehicle):
        """ Extract the information from the WSDL and build a vehicle of type
        Vehicle.

        Input:
            etree_vehicle :: xml.etree.ElementTree

        Return:
            vehicle :: [Vehicle, ...]
        """
        find = lambda tag: self._attr_lookup(etree_vehicle, tag)
        vehicle = Vehicle()

        vehicle.accident_free = find('a:accident_free')
        vehicle.body_colorgroup_id = find('a:body_colorgroup_id')
        vehicle.body_id = find('a:body_id')
        vehicle.brand_id = find('a:brand_id')
        vehicle.category_id = find('a:category_id')
        etree_equipment_ids =\
                etree_vehicle.findall('a:equipments/a:equipment_id',\
                                      self.name_spaces)
        vehicle.equipment_ids = self._equipments_factory(etree_equipment_ids)
        vehicle.fuel_type_id = find('a:fuel_type_id')
        vehicle.gear_type_id = find('a:gear_type_id')
        vehicle.initial_registration_raw = find('a:initial_registration')
        vehicle.kilowatt = find('a:kilowatt')
        all_images =\
                etree_vehicle.findall('a:media/a:images/a:image/a:uri',\
                                  self.name_spaces)
        vehicle.all_images = self._images_factory(all_images)
        vehicle.media_image_count = find('a:media/a:x_code/a:image_count')
        vehicle.mileage = find('a:mileage')
        vehicle.model_id = find('a:model_id')
        vehicle.price = find('a:prices/a:price/a:value')
        vehicle.currency = find('a:prices/a:price/a:currency_id')
        vehicle.vehicle_guid = find('a:vehicle_guid')
        vehicle.vehicle_id = find('a:vehicle_id')
        vehicle.version = find('a:version')
        vehicle.consumption = find('./a:consumption/a:liquid/a:combined')
        vehicle.extra_urban = find('./a:consumption/a:liquid/a:extra_urban')
        vehicle.urban = find('./a:consumption/a:liquid/a:urban')
        vehicle.capacity = find('a:capacity')
        vehicle.cylinder = find('a:cylinder')
        vehicle.doors = find('a:doors')
        vehicle.emiss_class_id = find('./a:emission/a:class_id')
        vehicle.emiss_co2_liquid = find('./a:emission/a:co2_liquid')
        vehicle.notes = find('a:notes')
        vehicle.seats = find('a:seats')
        vehicle.gears = find('a:gears')
        vehicle.kerb_weight = find('a:kerb_weight')
        vehicle.avail_begin = find('./a:availability/a:begin')
        vehicle.avail_last_change = find('./a:availability/a:last_change')

        return vehicle

    def _vehicles_factory(self, etree_vehicles):
        """ Build a list of vehicules of type Vehicle

        Input:
            etree_vehicles :: [v0 :: xml.etree.ElementTree.Element, ...]

        Returns:
            vehicules :: [v0 :: Vehicule, ...]
        """
        vehicles = list()
        for etree_v in etree_vehicles:
            find = lambda tag: self._attr_lookup(etree_v, tag)
            vehicle = self._vehicle_factory(etree_v)

            vehicle.body_painting_id = find('a:body_painting_id')
            vehicle.media_image_feature = find('a:media/a:images/a:image/a:uri')
            vehicle.owners_offer_key = find('a:owners_offer_key')
            vehicles.append(vehicle)

        return vehicles

    def _attr_lookup(self, etree, tag):
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

    def _equipments_factory(self, etree_equipment_ids):
        """ Return a list of equipments

        Input:
            etree_equipment_ids :: [e0 :: xml.etree.ElementTree.Element, ...]
        """
        return [e.text for e in etree_equipment_ids]

    def _images_factory(self, etree_images):
        """ Return a list of images """
        return [e.text for e in etree_images]


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
        self.all_images = None
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
        self.capacity = None
        self.cylinder = None
        self.seats = None
        self.doors = None
        self.extra_urban = None
        self.urban = None
        self.notes = None
        self.gears = None
        self.kerb_weight = None

    def __str__(self): # pragma: no cover
        """ Representation of the object"""
        return self.brand_id

    @property
    def category(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='category', item_id=self.category_id).text

    @property
    def body_color(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='body_color', item_id=self.body_colorgroup_id).text

    @property
    def body(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='body', item_id=self.body_id).text

    @property
    def country(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def culture(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def lookup_currency(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def customer_type(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def equipments(self): # pragma: no cover
        """ Return name of the equipments (not the id) """
        return [Enumeration.objects.get(name='equipment',\
                    item_id=eid).text for eid in self.equipment_ids]

    @property
    def fraud_reason(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def fuel(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='fuel', item_id=self.fuel_type_id).text

    @property
    def gear_types(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='gear_types', item_id=self.gear_type_id).text

    @property
    def body_painting(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='body_painting', item_id=self.body_painting_id).text

    @property
    def seal(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def seal_class(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def service(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def phonenumber_type(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def emission_class(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='emission_class', item_id=self.emiss_class_id).text

    @property
    def vattype(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def visibilitytype(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def emission_sticker(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def allfueltype(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def brand(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='brand', item_id=self.brand_id).text

    @property
    def model_line(self): # pragma: no cover
        """ Retrieve data from the database """
        return NotImplemented

    @property
    def model(self): # pragma: no cover
        """ Retrieve data from the database """
        return Enumeration.objects.get(name='model', item_id=self.model_id).text

    @property
    def initial_registration(self):
        """ Reformat the date of the first registration """
        return datetime.strptime(self.initial_registration_raw,\
                                 '%Y-%m-%dT%H:%M:%S').strftime('%m/%y')

def filter_brands(vehicles):
    """ Group the cars by brands """
    brands = defaultdict(int)
    for vhc in vehicles:
        brands[vhc.brand] += 1
    return dict(brands)
