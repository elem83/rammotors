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

