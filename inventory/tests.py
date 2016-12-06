"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from inventory.views import vehicules


# Create your tests here.

class VehiculeTest(TestCase):
    """Testing the vehicules application """

    def test_vehicules_url_resolve(self):
        """Resolve the vehicules URL"""
        found = resolve('/vehicules/')
        self.assertEqual(found.func, vehicules)

    def test_vehicules_return_html(self):
        """Testing that we get an html"""
        request = HttpRequest()
        response = vehicules(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Vehicules</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))


