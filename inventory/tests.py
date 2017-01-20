"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from inventory.views import vehicules_list
from inventory import services


# Create your tests here.

class VehiculeTest(TestCase):
    """Testing the vehicules application """

    def setUp(self):
        """ Setup response for further tests"""
        # http request/response
        self.wsdl_autoscout24 = services.WsdlAutoscout24()
        self.response = self.wsdl_autoscout24.response

    def test_vehicules_url_resolve(self):
        """Resolve the vehicules URL"""
        found = resolve('/')
        self.assertEqual(found.func, vehicules_list)

    def test_vehicules_return_html(self):
        """Testing that we get an html"""
        request = HttpRequest()
        response = vehicules_list(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>Ram Motors</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>\n'))

    def test_wsdl_findallarticles(self):
        """Testing the wsdl query to fetch the list of cars"""
        self.assertTrue(self.response.status_code, 200)
        self.assertTrue(self.response.content.startswith(b'<s:Envelope'))
        self.assertTrue(\
        self.response.content.endswith(\
            b'</FindArticlesResponse></s:Body></s:Envelope>'))

    def test_etree_vehicules(self):
        """ test etree_vehicles """
        etree_vehicles = self.wsdl_autoscout24.etree_vehicles()
        self.assertEqual(type(etree_vehicles), list)

    def test_vehicles_factory(self):
        """ Return a list of id """
        etree_vehicles = self.wsdl_autoscout24.etree_vehicles()
        vehicles = self.wsdl_autoscout24.vehicles_factory(etree_vehicles)
        self.assertNotEqual(len(vehicles), 0)
        self.assertEqual(type(vehicles[0]), services.Vehicle)
        self.assertEqual(type(vehicles[0].brand_id), str)


