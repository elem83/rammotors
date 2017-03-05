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

reported_cars = lambda browser: \
        int(browser.find_element_by_id('count_car').text)

def visible_cars(browser, css_selector): \
    return len([x for x in \
        browser.find_elements_by_class_name('list-product-description') \
        if x.is_displayed()])

def reset(browser):
    browser.get('http://localhost:8000')

def assert_title(browser):
    assert 'Ram Motors' in browser.title,\
    'Browse title was: ' + browser.title

def wait_for_count(browser, css_selector):
    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)) \
        and visible_cars(browser, css_selector) == reported_cars(browser))

def assert_reported_vs_listed(browser, css_selector):
    assert visible_cars(browser, css_selector) == reported_cars(browser), \
    "The number of cars reported should be equal to the number of cars display"

def move_to(browser, css_selector):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )

    browser.find_element_by_css_selector(css_selector).click()

def test_browsing_check(browser):
    """ Docstring """
    reset(browser)
    assert_title(browser)
    assert_reported_vs_listed(browser, 'list-product-description')
    move_to(browser, 'ul.list-inline a[href="/grid/"]')
    assert_reported_vs_listed(browser, 'div.filter-results div.col-md-4')
    move_to(browser, 'ul.list-inline a[href="/"]')
    assert_reported_vs_listed(browser, 'list-product-description')


def test_filters(browser):
    reset(browser)
    move_to(browser, 'li > label.checkbox')
    wait_for_count(browser, 'list-product-description')
    assert_reported_vs_listed(browser, 'list-product-description')
