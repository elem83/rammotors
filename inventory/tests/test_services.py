# pylint: disable=missing-docstring, unused-import, redefined-outer-name
"""Unit test for Inventory"""

from xml.etree import ElementTree
import pytest

from inventory.views import vehicles_list
from inventory import services

@pytest.fixture()
def fixture_soap():
    wsdl_autoscout24 = services.AS24WSSearch()
    response = wsdl_autoscout24.find_articles()
    return {'as': wsdl_autoscout24, 'response': response}

def check_obj_not_empty(obj):
    """ Check that the content of the object instance has been filled with
    value.

    Input:
        obj :: Any object instance

    Return:
        False if all value attribute are None
    """
    return any(obj.__dict__.values())

def test_list_vehicles(fixture_soap):
    result = fixture_soap['as'].list_vehicles()
    assert isinstance(result, list), \
            "Should return a list"
    assert isinstance(result[0], services.Vehicle), \
            "Should return a list of Vehicle"
    empty_vehicle = services.Vehicle()
    assert not check_obj_not_empty(empty_vehicle), \
            "This empty vehicle should be empty"
    assert check_obj_not_empty(result[0]), \
            "The first vehicle of the list should not be empty"
    assert all(check_obj_not_empty(obj) for obj in result), \
            "None of the vehicule should be empty"

def test_details_vehicle(fixture_soap):
    vehicle = fixture_soap['as'].list_vehicles()[0]
    vehicle_id = vehicle.vehicle_id
    assert isinstance(fixture_soap['as'].details_vehicle(vehicle_id), \
                      services.Vehicle), "It should be an instance of Vehicle"
    assert check_obj_not_empty(vehicle), "This instance should not be empty"

def test_uri(fixture_soap):
    # pylint: disable=unnecessary-lambda
    check = lambda x: fixture_soap['as'].uri_images(x)
    assert '/images/' in check('main'), \
            "Should return a URI containing /images/"
    assert '/images-big/' in check('big'), \
            "Should return a URI containing /images-big/"
    assert '/images-small/' in check('small'), \
            "Should return a URI containing /images-small/"
    assert '/thumbnails-big/' in check('thumb'), \
            "Should return a URI containing /thumbnails-big/"

def test_get_article_details(fixture_soap):
    scout = fixture_soap['as'].get_article_details('0')
    assert scout.status_code == 200, "Should return 200"
    assert 'NothingFound' in str(scout.content), \
            "Should contains the string NothingFound"
    vehicle = fixture_soap['as'].list_vehicles()[0]
    vehicle_id = vehicle.vehicle_id
    scout2 = fixture_soap['as'].get_article_details(vehicle_id)
    assert 'NothingFound' not in \
            str(scout2.content), \
            "Should not contains the string NothingFound"

def test_find_articles(fixture_soap):
    """Testing the wsdl query to fetch the list of cars"""
    assert fixture_soap['response'].status_code == 200, "Should return 200"
    assert fixture_soap['response'].content.startswith(b'<s:Envelope'), \
            "The Soap response should start with the Envelope tag"
    assert fixture_soap['response'].content.endswith(\
        b'</FindArticlesResponse></s:Body></s:Envelope>'), \
            "The Soap response should finished with FindArticles ..."

def test_etree_vehicles(fixture_soap):
    # pylint: disable=protected-access
    etree_vehicles = \
            fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    assert isinstance(etree_vehicles, list), "Should be a list"
    assert '{http://www.autoscout24.com/webapi/data/}vehicle' in \
        str(etree_vehicles[0]), "Should be a ElementTree"

"""
    def test_vehicles_factory(self):
        etree_vehicles = self.wsdl_autoscout24._etree_vehicles(self.response.content)
        vehicles = services.AS24WSSearch()._vehicles_factory(etree_vehicles)
        assertNotEqual(len(vehicles), 0)
        assertEqual(type(vehicles[0]), services.Vehicle)
        assertEqual(type(vehicles[0].brand_id), str)

"""
