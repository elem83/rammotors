"""Unit test for Inventory"""

from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):
    """ Unit test for Inventory """
    def test_bad_maths(self):
        """ Test the django testing module """
        self.assertEqual(1+1, 3)

