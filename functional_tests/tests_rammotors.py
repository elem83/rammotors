# pylint: disable=unused-argument, redefined-outer-name, missing-docstring
"""
Functional testing for Ram Motors
"""

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser(request):
    selenium = webdriver.Firefox()
    selenium.implicitly_wait(3)
    selenium.set_window_size(1000, 800)
    browser.get('http://localhost:8000')
    def teardown():
        selenium.quit()
    request.addfinalizer(teardown)
    return selenium

# def test_list_cars(browser):
def test_browsing_check(browser):
    """ Docstring """

    assert 'Ram Motors' in browser.title,\
    'Browse title was: ' + browser.title

    count_car = int(browser.find_element_by_id('count_car').text)

    list_cars = \
        len(browser.find_elements_by_class_name('list-product-description'))
    assert list_cars == count_car, \
    "The number of cars reported should be equal to the number of cars display"

    browser.find_element_by_css_selector('ul.list-inline a[href="/grid/"]').click()
    grid_cars = \
    len(browser.find_elements_by_css_selector('div.filter-results div.col-md-4'))
    assert grid_cars == count_car, \
            "The number of cars in the grid should match the number of cars"

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.list-inline a[href="/"]'))
    )

    browser.find_element_by_css_selector('ul.list-inline a[href="/"]').click()
    list_cars = \
        len(browser.find_elements_by_class_name('list-product-description'))
    assert list_cars == count_car, \
            "The number of cars in the list should match the number of cars"
