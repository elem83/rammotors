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

def visible_cars(browser, css_selector):
    return len([x for x in \
        browser.find_elements_by_class_name(css_selector) \
        if x.is_displayed()])

def assert_title(browser):
    assert 'Ram Motors' in browser.title,\
    'Browse title was: ' + browser.title

def wait_for_count(browser, css_selector):
    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)) \
        and visible_cars(browser, css_selector) == reported_cars(browser))

def assert_reported_vs_visible(browser, css_selector):
    assert visible_cars(browser, css_selector) == reported_cars(browser), \
    "The number of cars reported should be equal to the number of cars display"

def test_links(browser):
    browser.get('http://localhost:8000/grid/')

    browser.find_element_by_css_selector('ul.list-inline a[href="/grid/"]').click()
    assert_title(browser)
    browser.find_element_by_css_selector('ul.list-inline a[href="/"]').click()
    assert_title(browser)

def helper_filters(browser, css_selector_count):

    filters = browser.find_elements_by_css_selector('li > label.checkbox')
    assert len(filters) != 0, 'The number of filters should not be null'
    for f in filters:
        f.click()
        wait_for_count(browser, css_selector_count)
        assert_reported_vs_visible(browser, css_selector_count)

    browser.find_element_by_id('reset').click()
    assert_reported_vs_visible(browser, css_selector_count)

def helper_sort(browser, css_id_key, css_selector_count, page='list'):

    browser.find_element_by_id('sort_criteria').click()
    browser.find_element_by_css_selector('li[data-sort-by="{}"]'.format(css_id_key)).click()

    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CLASS_NAME, css_id_key)) \
        and visible_cars(browser, css_selector_count) == reported_cars(browser))

    if page == 'list':
        elems_raw = [(x.location['y'], int(x.text.replace(",", ""))) for x in \
                browser.find_elements_by_class_name(css_id_key)]

        elems = [x[1] for x in sorted(elems_raw, key=lambda pos: pos[0])]
        assert all(elems[i] <= elems[i+1] for i in range(len(elems)-1)), \
            "The list should be sorted"
    else: # grid
        elems_raw = [(x.location['x'], x.location['y'], int(x.text.replace(",", ""))) for x in \
                browser.find_elements_by_class_name('km')]

        elems = [x[2] for x in sorted(elems_raw, key=lambda pos: (pos[1], pos[0]))]
        assert all(a <= b  for a, b in zip(elems, elems[:1])), \
        'The list should be sorted'

def test_list_pages(browser):
    browser.get('http://localhost:8000')

    css_selector_count = 'list-product-description'
    # Test entry page
    assert_reported_vs_visible(browser, css_selector_count)

    # Test filters
    helper_filters(browser, css_selector_count)

    # Test sort km
    helper_sort(browser, 'km', css_selector_count)

    # Test sort price
    helper_sort(browser, 'price', css_selector_count)

def test_grid_pages(browser):
    browser.get('http://localhost:8000/grid/')
    assert_title(browser)

    css_selector_count = 'product-description'

    # Test entry page
    assert_reported_vs_visible(browser, css_selector_count)

    # Test filters
    helper_filters(browser, css_selector_count)

    # Test sort km
    helper_sort(browser, 'km', css_selector_count, page='grid')

    # Test sort price
    helper_sort(browser, 'price', css_selector_count, page='grid')
