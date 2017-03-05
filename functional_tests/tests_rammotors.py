# pylint: disable=invalid-name, unused-argument, redefined-outer-name, missing-docstring
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
    def teardown():
        selenium.quit()
    request.addfinalizer(teardown)
    return selenium

def home(browser):
    browser.get('http://localhost:8000')

def assert_title(browser):
    assert 'Ram Motors' in browser.title,\
    'Browse title was: ' + browser.title

def move_to(browser, css_selector):
    browser.find_element_by_css_selector(css_selector).click()

reported_cars = lambda browser: \
        int(browser.find_element_by_id('count_car').text)

visible_cars = lambda browser, css_selector: \
        len(browser.find_elements_by_class_name('list-product-description'))

def test_browsing_check(browser):
    """ Docstring """
    home(browser)
    assert_title(browser)

    assert visible_cars(browser, 'list-product-description') == reported_cars(browser), \
    "The number of cars reported should be equal to the number of cars display"

    move_to(browser, 'ul.list-inline a[href="/grid/"]')

    assert visible_cars(browser, 'div.filter-results div.col-md-4') == reported_cars(browser), \
    "The number of cars reported should be equal to the number of cars display"

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.list-inline a[href="/"]'))
    )

    move_to(browser, 'ul.list-inline a[href="/"]')
    assert visible_cars(browser, 'list-product-description') == reported_cars(browser), \
    "The number of cars reported should be equal to the number of cars display"
