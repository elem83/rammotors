"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from inventory.views import vehicules_list


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
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Ram Motors</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))


