# pylint: disable=redefined-outer-name, missing-docstring, unused-argument, no-member, protected-access
"""Unit test for Inventory"""

from unittest.mock import patch

from mixer.backend.django import mixer
import pytest # pylint: disable=unused-import

from django.urls import resolve
from django.test import RequestFactory
#from django.template.loader import render_to_string

from inventory import views
from inventory import services
from inventory.tests.test_services import (get_lookup_mock, find_articles_mock,
                                           get_article_mock)

pytestmark = pytest.mark.django_db # pylint: disable=invalid-name

@pytest.fixture(scope="function")
def db_enum():
    for elem in services.AS24WSSearch().get_lookup_data():
        mixer.blend('inventory.Enumeration', **elem)

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_vehicles_list(mock_find_articles, mock_lookup):
    """Resolve the vehicles URL"""
    found = resolve('/')
    assert found.func == views.vehicles_list, \
            "Should find the list of vehicles"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_vehicles_grid(mock_find_articles, mock_lookup):
    """Resolve the vehicles URL"""
    found = resolve('/grid/')
    assert found.func == views.vehicles_grid, \
            "Should find the list of vehicles"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_grid_anonymous(mock_find_articles, mock_lookup, db_enum):
    request = RequestFactory().get('/grid/')
    response = views.vehicles_grid(request)
    assert response.status_code == 200, \
            "Should be callable by anyone"
    assert response.content.startswith(b'\n<!DOCTYPE html>'), \
        "Should return a valid HTML5"
    assert response.content.endswith(b'</html>\n'), \
        "Should return a valid HTML5"
    assert b'<title>Ram Motors</title>' in response.content, \
        "Should contain the title expected"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_list_anonymous(mock_find_articles, mock_lookup, db_enum):
    request = RequestFactory().get('/')
    response = views.vehicles_list(request)
    assert response.status_code == 200, \
            "Should be callable by anyone"
    assert response.content.startswith(b'\n<!DOCTYPE html>'), \
        "Should return a valid HTML5"
    assert response.content.endswith(b'</html>\n'), \
        "Should return a valid HTML5"
    assert b'<title>Ram Motors</title>' in response.content, \
        "Should contain the title expected"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.get_article_details', side_effect=get_article_mock)
def test_vehicles_details(mock_get_article_details, db_enum):
    found = resolve('/car/306739943')
    assert found.func == views.vehicle_details, \
            "Should find the vehicles details"
    request = RequestFactory().get('/car/306739943')
    response = views.vehicle_details(request, 306739943)
    assert response.status_code == 200, \
            "Should be callable by anyone"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.get_article_details', side_effect=get_article_mock)
def test_vehicles_does_not_exist(mock_get_article_details, db_enum):
    request = RequestFactory().get('/car/0')
    response = views.vehicle_details(request, 0)
    assert response.status_code == 404, \
            "If the vehicle does not exist it should throw a 404 error page"
