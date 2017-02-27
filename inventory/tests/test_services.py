# pylint: disable=missing-docstring, unused-import, redefined-outer-name
"""Unit test for Inventory"""

import pytest

from inventory.views import vehicles_list
from inventory import services

@pytest.fixture()
def fixture_soap():
    wsdl_autoscout24 = services.AS24WSSearch()
    response = wsdl_autoscout24.find_articles()
    return {'response': response}

def test_find_articles(fixture_soap):
    """Testing the wsdl query to fetch the list of cars"""
    assert fixture_soap['response'].status_code == 200, "Should return 200"
    assert fixture_soap['response'].content.startswith(b'<s:Envelope'), \
            "The Soap response should start with the Envelope tag"
    assert fixture_soap['response'].content.endswith(\
        b'</FindArticlesResponse></s:Body></s:Envelope>'), \
            "The Soap response should finished with FindArticles ..."
"""
    def test_etree_vehicles(self):
        etree_vehicles = services.AS24WSSearch()._etree_vehicles(self.response.content)
        assertEqual(type(etree_vehicles), list)

    def test_vehicles_factory(self):
        etree_vehicles = self.wsdl_autoscout24._etree_vehicles(self.response.content)
        vehicles = services.AS24WSSearch()._vehicles_factory(etree_vehicles)
        assertNotEqual(len(vehicles), 0)
        assertEqual(type(vehicles[0]), services.Vehicle)
        assertEqual(type(vehicles[0].brand_id), str)

    def test_uri(self):
        images_uri = self.wsdl_autoscout24.uri_images('main')
        assertEqual(images_uri, 'http://pic.autoscout24.net/images/')
"""
