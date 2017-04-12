# pylint: disable=unused-argument, invalid-name, protected-access, missing-docstring, unused-import, redefined-outer-name
"""Unit test for Inventory"""

from os.path import join
from xml.etree import ElementTree
from re import search
from unittest.mock import patch

import requests
import requests_mock

import pytest

from mixer.backend.django import mixer

from inventory.views import vehicles_list
from inventory import services
from rammotors.settings import test as settings

def get_article_mock(*args):
    status_code = 200
    if args[0] == 'notinlist':
        content = str.encode(\
        open('inventory/tests/soap_vehicle_details_response_nothing.xml').read())
    else:
        content = str.encode(\
        open('inventory/tests/soap_vehicle_details_response.xml').read())

    with requests_mock.Mocker() as m:
        m.get('https://api.mock_scout.com', status_code=status_code, \
              content=content)
        response = requests.get('https://api.mock_scout.com')

    return response

def find_articles_mock(*args, **kwargs):
    status_code = 200
    content = str.encode(\
    open('inventory/tests/soap_find_articles_response.xml').read())
    with requests_mock.Mocker() as m:
        m.get('https://api.mock_scout.com', status_code=status_code, \
              content=content)
        response = requests.get('https://api.mock_scout.com')
    return response

def get_lookup_mock(*args, **kwargs):
    content = str.encode(\
    open('inventory/tests/soap_lookup_response.xml').read())
    with requests_mock.Mocker() as m:
        m.get('https://api.mock_scout.com', content=content)
        response = requests.get('https://api.mock_scout.com')
    return response

def check_obj_not_empty(obj):
    """ Check that the content of the object instance has been filled with
    value.

    Input:
        obj :: Any object instance

    Return:
        False if all value attribute are None
    """
    return any(obj.__dict__.values())

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_list_vehicles(mock_find_articles):
    result = services.AS24WSSearch().list_vehicles()
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

@patch('inventory.services.get_article_details', side_effect=get_article_mock)
def test_details_vehicle(mock_get_article_details):
    vehicle = services.AS24WSSearch().details_vehicle(3455334)
    assert isinstance(vehicle, \
                      services.Vehicle), "It should be an instance of Vehicle"
    assert check_obj_not_empty(vehicle), "This instance should not be empty"

def test_uri():
    # pylint: disable=unnecessary-lambda
    check = lambda x: services.AS24WSSearch().uri_images(x)
    assert '/images/' in check('main'), \
            "Should return a URI containing /images/"
    assert '/images-big/' in check('big'), \
            "Should return a URI containing /images-big/"
    assert '/images-small/' in check('small'), \
            "Should return a URI containing /images-small/"
    assert '/thumbnails-big/' in check('thumb'), \
            "Should return a URI containing /thumbnails-big/"
    with pytest.raises(ValueError):
        check('anything')

@patch('inventory.services.get_article_details', side_effect=get_article_mock)
def test_get_article_details(mock_get_article_details):
    scout = services.get_article_details('notinlist')
    assert scout.status_code == 200, "Should return 200"
    assert 'NothingFound' in str(scout.content), \
            "Should contains the string NothingFound"
    scout2 = services.get_article_details(389889)
    assert 'NothingFound' not in \
            str(scout2.content), \
            "Should not contains the string NothingFound"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_find_articles(mock_find_articles):
    """Testing the wsdl query to fetch the list of cars"""
    response = services.find_articles()
    assert response.status_code == 200, "Should return 200"
    assert response.content.startswith(b'<s:Envelope'), \
            "The Soap response should start with the Envelope tag"
    assert response.content.endswith(b'</s:Envelope>\n'), \
            "The Soap response should finished with FindArticles ..."

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_etree_vehicles(mock_find_articles):
    etree_vehicles = \
    services.AS24WSSearch()._etree_vehicles(services.find_articles().content)
    assert isinstance(etree_vehicles, list), "Should be a list"
    assert isinstance(etree_vehicles[0], ElementTree.Element), \
            "Should be a ElementTree"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_vehicle_factory(mock_find_articles):
    etree_vehicles = \
        services.AS24WSSearch()._etree_vehicles(services.find_articles().content)
    vehicle = services.AS24WSSearch()._vehicle_factory(etree_vehicles[0])
    assert isinstance(vehicle, services.Vehicle), "Should be type of Vehicle"
    assert isinstance(vehicle.brand_id, str), \
            "Brand should be filled with a value"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_vehicles_factory(mock_find_articles):
    etree_vehicles = \
    services.AS24WSSearch()._etree_vehicles(services.find_articles().content)
    vehicles = services.AS24WSSearch()._vehicles_factory(etree_vehicles)
    assert check_obj_not_empty(vehicles[0]), \
            "The first vehicle of the list should not be empty"
    assert all(check_obj_not_empty(obj) for obj in vehicles), \
            "None of the vehicule should be empty"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_attr_lookup(mock_find_articles):
    etree_vehicles = \
    services.AS24WSSearch()._etree_vehicles(services.find_articles().content)
    assert services.AS24WSSearch()._attr_lookup(etree_vehicles[0], 'a:brand_id') != \
            '00', "The brand should not be equal to 00"
    assert services.AS24WSSearch()._attr_lookup(etree_vehicles[0], 'a:not_exist') == \
            '', "Should be the empty string"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_equipments_factory(mock_find_articles):
    etree_vehicles = \
    services.AS24WSSearch()._etree_vehicles(services.find_articles().content)

    etree_equipment_ids = \
            etree_vehicles[0].findall('a:equipments/a:equipment_id',\
                                    services.AS24WSSearch().name_spaces)
    result = services.AS24WSSearch()._equipments_factory(\
                                            etree_equipment_ids)
    assert isinstance(result, list), "Should be an instance of list"
    assert all(isinstance(int(item), int) for item in result), \
            "Should contains number or nothing"
    assert all(isinstance(int(item), int) for item in []), \
            "Should contains number or nothing"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_images_factory(mock_find_articles):
    etree_vehicles = \
        services.AS24WSSearch()._etree_vehicles(services.find_articles().content)
    all_images = \
            etree_vehicles[0].findall('a:media/a:images/a:image/a:uri',\
                                services.AS24WSSearch().name_spaces)
    result = services.AS24WSSearch()._images_factory(all_images)
    assert isinstance(result, list), "Should be an instance of list"
    assert all('.jpg' in item for item in result), \
            "Should contains images"

@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_initial_registration(mock_find_articles):
    vehicle = services.AS24WSSearch().list_vehicles()[0]
    assert isinstance(vehicle.initial_registration, str), \
            "The date should be of type string"
    assert search(r'\d\d/\d\d', vehicle.initial_registration), \
            "The date should have the format mm/yy"

@pytest.mark.django_db
@patch('inventory.services.lookup', side_effect=get_lookup_mock)
@patch('inventory.services.find_articles', side_effect=find_articles_mock)
def test_filter_brands(mock_find_articles, mock_lookup):
    for elem in services.AS24WSSearch().get_lookup_data():
        mixer.blend('inventory.Enumeration', **elem)
    vehicles = services.AS24WSSearch().list_vehicles()
    brands = services.filter_brands(vehicles)
    assert isinstance(brands, dict), "Should return a dictionary"
    assert all([value for value in brands.values()]), \
            "No value should be equal to nothing"

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
def test_get_enumerations(mock_lookup):
    result = services.AS24WSSearch().get_lookup_data()
    assert isinstance(result, list), "Should return a dict"
    assert isinstance(result[0], dict), \
            "The elements of the list should be dict"
    assert all([all(elem.values()) for elem in result])
    assert len(result) != 0, \
            "The number of elements is not null"

def test__parse_xml():
    soap_response = open('inventory/tests/soap_lookup_response.xml').read()
    assert isinstance(services.AS24WSSearch()._parse_xml(soap_response), \
                     ElementTree.Element)

def test_get_username_password_file():
    username = services.USERNAME
    password = services.PASSWORD
    assert len(username) != 0
    assert len(password) != 0
