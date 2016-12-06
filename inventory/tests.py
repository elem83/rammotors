"""Unit test for Inventory"""

from django.urls import resolve
from django.test import TestCase
from inventory.views import vehicules


# Create your tests here.

class VehiculeTest(TestCase):
    """Testing the vehicules application """

    def test_vehicules_url_resolve(self):
        """Resolve the vehicules URL"""
        found = resolve('/vehicules/')
        self.assertEqual(found.func, vehicules)
