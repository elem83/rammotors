# pylint: disable=unused-argument, no-member, protected-access
"""Unit test for Inventory"""

from unittest.mock import patch

from mixer.backend.django import mixer
import pytest # pylint: disable=unused-import

from django.urls import resolve
from django.test import RequestFactory
#from django.http import HttpRequest
#from django.template.loader import render_to_string

from inventory.views import vehicles_list
from inventory import services
from inventory.tests.test_services import (get_lookup_mock, find_articles_mock,
                                           get_article_mock)


pytestmark = pytest.mark.django_db # pylint: disable=invalid-name

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_vehicles_url_resolve(mock_find_articles, mock_lookup):
    """Resolve the vehicles URL"""
    for elem in services.AS24WSSearch().get_lookup_data():
        mixer.blend('inventory.Enumeration', **elem)
    found = resolve('/')
    assert found.func == vehicles_list, \
            "Should find the list of vehicles"
    request = RequestFactory().get('/')
    response = vehicles_list(request)
    assert response.status_code == 200, \
            "Should be callable by anyone"
"""
@patch('inventory.services.get_article_details', side_effect=get_article_mock)
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
