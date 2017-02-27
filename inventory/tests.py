# pylint: disable=protected-access
"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from inventory.views import vehicles_list
from inventory import services


# Create your tests here.

class VehiculeTest(TestCase):
    """Testing the vehicles application """

    def setUp(self):
        """ Setup response for further tests"""
        # http request/response
        self.wsdl_autoscout24 = services.AS24WSSearch()
        self.response = self.wsdl_autoscout24.find_articles()

    def test_vehicles_url_resolve(self):
        """Resolve the vehicles URL"""
        found = resolve('/')
        self.assertEqual(found.func, vehicles_list)

    def test_vehicles_return_html(self):
        """Testing that we get an html"""
        request = HttpRequest()
        response = vehicles_list(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>Ram Motors</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>\n'))

    def test_vehicles_return_html2(self):
        """Testing that we get an html"""
        request = HttpRequest()
        response = vehicles_list(request)
        autoscout = services.AS24WSSearch()
        images_uri = autoscout.uri_images('main')
        vehicles = autoscout.list_vehicles()
        brands = services.filter_brands(vehicles)
        context = {\
            'vehicles': vehicles,
            'images_uri': images_uri,
            'brands': brands\
        }
        expected_html = render_to_string('inventory/list_cars.html', context)
        self.assertEqual(response.content.decode(), expected_html)

    # Unit test

    def test_find_articles(self):
        """Testing the wsdl query to fetch the list of cars"""
        self.assertTrue(self.response.status_code, 200)
        self.assertTrue(self.response.content.startswith(b'<s:Envelope'))
        self.assertTrue(\
        self.response.content.endswith(\
            b'</FindArticlesResponse></s:Body></s:Envelope>'))

    def test_etree_vehicles(self):
        """ test _etree_vehicles """
        etree_vehicles = services.AS24WSSearch()._etree_vehicles(self.response.content)
        self.assertEqual(type(etree_vehicles), list)

    def test_vehicles_factory(self):
        """ test the factory """
        etree_vehicles = self.wsdl_autoscout24._etree_vehicles(self.response.content)
        vehicles = services.AS24WSSearch()._vehicles_factory(etree_vehicles)
        self.assertNotEqual(len(vehicles), 0)
        self.assertEqual(type(vehicles[0]), services.Vehicle)
        self.assertEqual(type(vehicles[0].brand_id), str)

    def test_uri(self):
        """ Test the uri_images method """
        images_uri = self.wsdl_autoscout24.uri_images('main')
        self.assertEqual(images_uri, 'http://pic.autoscout24.net/images/')

