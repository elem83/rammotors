# pylint: disable=no-member, protected-access
"""Unit test for Inventory"""

from django.urls import resolve
from django.test import RequestFactory
#from django.http import HttpRequest
#from django.template.loader import render_to_string

import pytest # pylint: disable=unused-import

from inventory.views import vehicles_list

pytestmark = pytest.mark.django_db # pylint: disable=invalid-name

@pytest.mark.xfail(run=False)
def test_vehicles_url_resolve():
    """Resolve the vehicles URL"""
    found = resolve('/')
    assert found.func == vehicles_list, \
            "Should find the list of vehicles"
    request = RequestFactory().get('/')
    response = vehicles_list(request)
    assert response.status_code == 200, \
            "Should be callable by anyone"
"""
def test_vehicles_return_html()
    request = HttpRequest()
    response = vehicles_list(request)
    self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
    self.assertIn(b'<title>Ram Motors</title>', response.content)
    self.assertTrue(response.content.endswith(b'</html>\n'))

def test_vehicles_return_html2():
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
"""
