# pylint: disable=unused-import, no-self-use, too-few-public-methods
"""Unit test for Inventory"""

import pytest

from inventory.views import vehicles_list
from inventory import services

class VehiculeTest:
    """Testing the vehicles application """

    def test_find_articles(self):
        """Testing the wsdl query to fetch the list of cars"""
        wsdl_autoscout24 = services.AS24WSSearch()
        response = wsdl_autoscout24.find_articles()
        assert response.status_code == 200, "Should return 200"
"""
        assertTrue(self.response.content.startswith(b'<s:Envelope'))
        assertTrue(\
        self.response.content.endswith(\
            b'</FindArticlesResponse></s:Body></s:Envelope>'))

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
