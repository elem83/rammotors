"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from inventory.views import vehicules_list
from inventory import services


# Create your tests here.

class VehiculeTest(TestCase):
    """Testing the vehicules application """

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
        response = services.wsdl_findallarticles()
        self.assertTrue(response.status_code, 200)
