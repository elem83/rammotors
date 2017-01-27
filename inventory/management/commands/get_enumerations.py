""" Retrieve lookup value from Autocout24 """

import xml.etree.ElementTree as ET
import requests

from django.core.management.base import BaseCommand
from inventory.models import Enumeration


URL = 'http://api.autoscout24.com/AS24_WS_Lookup'

USERNAME = 'BE_2142129754'
PASSWORD = 'netsarammo2017$'
SELLER_ID = '2142129754'

NAME_SPACE = {'s':'http://schemas.xmlsoap.org/soap/envelope/',
              'default': 'http://www.autoscout24.com/webapi/}',
              'a': 'http://www.autoscout24.com/webapi/data/'}
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
    return response.content

def parse_xml(response):
    """ Parse the XML received from the lookup """
    root = ET.fromstring(response)
    elements = root.find('.//a:elements', NAME_SPACE)
    return elements

def attr(element):
    """ Helper to fill retrieve all element from the enumeration.xml """
    name = element.find('a:name', NAME_SPACE).text
    item_id = element.find('a:id', NAME_SPACE).text
    item_text = element.find('a:text', NAME_SPACE).text
    return {'name': name, 'item_id': item_id, 'text': item_text}

def fill_db(elements):
    """ Fill the database """
    for elem in elements:
        Enumeration.objects.create(**attr(elem))


class Command(BaseCommand):
    """ Retrieve enumeration from Autoscout24 """
    help = 'Retrieve enumeration from Autoscout24'

    def handle(self, *args, **options):
        """ Mandatory method """
        fill_db(parse_xml(lookup()))
