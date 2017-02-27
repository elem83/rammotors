# pylint: disable=protected-access, missing-docstring, unused-import, redefined-outer-name
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
    etree_vehicles = \
            fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    assert isinstance(etree_vehicles, list), "Should be a list"
    assert '{http://www.autoscout24.com/webapi/data/}vehicle' in \
        str(etree_vehicles[0]), "Should be a ElementTree"

def test_vehicle_factory(fixture_soap):
    etree_vehicles = \
        fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    vehicle = fixture_soap['as']._vehicle_factory(etree_vehicles[0])
    assert isinstance(vehicle, services.Vehicle), "Should be type of Vehicle"
    assert isinstance(vehicle.brand_id, str), \
            "Brand should be filled with a value"

def test_vehicles_factory(fixture_soap):
    etree_vehicles = \
        fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    vehicles = fixture_soap['as']._vehicles_factory(etree_vehicles)
    assert check_obj_not_empty(vehicles[0]), \
            "The first vehicle of the list should not be empty"
    assert all(check_obj_not_empty(obj) for obj in vehicles), \
            "None of the vehicule should be empty"

def test_attr_lookup(fixture_soap):
    etree_vehicles = \
        fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    assert fixture_soap['as']._attr_lookup(etree_vehicles[0], 'a:brand_id') != \
            '00', "The brand should not be equal to 00"
    assert fixture_soap['as']._attr_lookup(etree_vehicles[0], 'a:not_exist') == \
            '', "Should be the empty string"

def test_equipments_factory(fixture_soap):
    etree_vehicles = \
        fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)

    etree_equipment_ids = \
            etree_vehicles[0].findall('a:equipments/a:equipment_id',\
                                    fixture_soap['as'].name_spaces)
    result = fixture_soap['as']._equipments_factory(\
                                            etree_equipment_ids)
    assert isinstance(result, list), "Should be an instance of list"
    assert all(isinstance(int(item), int) for item in result), \
            "Should contains number or nothing"
    assert all(isinstance(int(item), int) for item in []), \
            "Should contains number or nothing"

def test_images_factory(fixture_soap):
    etree_vehicles = \
        fixture_soap['as']._etree_vehicles(fixture_soap['response'].content)
    all_images = \
            etree_vehicles[0].findall('a:media/a:images/a:image/a:uri',\
                                fixture_soap['as'].name_spaces)
    result = fixture_soap['as']._images_factory(all_images)
    assert isinstance(result, list), "Should be an instance of list"
    assert all('.jpg' in item for item in result), \
            "Should contains images"
