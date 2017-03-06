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

# def move_to(browser, css_selector):
#    WebDriverWait(browser, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
#    )

def test_links(browser):
    browser.get('http://localhost:8000/grid/')

    browser.find_element_by_css_selector('ul.list-inline a[href="/grid/"]').click()
    assert_title(browser)
    browser.find_element_by_css_selector('ul.list-inline a[href="/"]').click()
    assert_title(browser)

def test_list_pages(browser):
    browser.get('http://localhost:8000')

    # Test entry page
    assert_reported_vs_visible(browser, 'list-product-description')

    # Test filters
    filters = browser.find_elements_by_css_selector('li > label.checkbox')
    assert len(filters) != 0, 'The number of filters should not be null'
    for f in filters:
        f.click()
        wait_for_count(browser, 'list-product-description')
        assert_reported_vs_visible(browser, 'list-product-description')

    browser.find_element_by_id('reset').click()
    assert_reported_vs_visible(browser, 'list-product-description')

    # Test sort km
    browser.find_element_by_id('sort_criteria').click()
    browser.find_element_by_css_selector('li[data-sort-by="km"]').click()

    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CLASS_NAME, 'km')) \
        and visible_cars(browser, 'list-product-description') == reported_cars(browser))

    elems_raw = [(x.location['y'], int(x.text.replace(",", ""))) for x in \
             browser.find_elements_by_class_name('km')]

    elems = [x[1] for x in sorted(elems_raw, key=lambda pos: pos[0])]
    assert all(elems[i] <= elems[i+1] for i in range(len(elems)-1)), \
        "The list should be sorted"

    # Test sort price
    browser.find_element_by_id('sort_criteria').click()
    browser.find_element_by_css_selector('li[data-sort-by="price"]').click()

    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CLASS_NAME, 'price')) \
        and visible_cars(browser, 'list-product-description') == reported_cars(browser))

    elems_raw = [(x.location['y'], int(x.text.replace(",", ""))) for x in \
             browser.find_elements_by_class_name('price')]

    elems = [x[1] for x in sorted(elems_raw, key=lambda pos: pos[0])]
    assert all(elems[i] <= elems[i+1] for i in range(len(elems)-1)), \
        "The list should be sorted"

def test_grid_pages(browser):
    browser.get('http://localhost:8000/grid/')
    assert_title(browser)

    # Test entry page
    assert_reported_vs_visible(browser, 'product-description')

    # Test filters
    filters = browser.find_elements_by_css_selector('li > label.checkbox')
    assert len(filters) != 0, 'The number of filters should not be null'
    for f in filters:
        f.click()
        wait_for_count(browser, 'product-description')
        assert_reported_vs_visible(browser, 'product-description')

    browser.find_element_by_id('reset').click()
    wait_for_count(browser, 'product-description')
    assert_reported_vs_visible(browser, 'product-description')

    # Test sort km
    browser.find_element_by_id('sort_criteria').click()
    browser.find_element_by_css_selector('li[data-sort-by="km"]').click()

    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CLASS_NAME, 'km')) \
        and visible_cars(browser, 'product-description') == reported_cars(browser))

    elems_raw = [(x.location['x'], x.location['y'], int(x.text.replace(",", ""))) for x in \
             browser.find_elements_by_class_name('km')]

    elems = [x[2] for x in sorted(elems_raw, key=lambda pos: (pos[1], pos[0]))]
    assert all(a <= b  for a, b in zip(elems, elems[:1])), \
     'The list should be sorted'

    # Test sort price
    browser.find_element_by_id('sort_criteria').click()
    browser.find_element_by_css_selector('li[data-sort-by="price"]').click()

    WebDriverWait(browser, 10).until(\
    lambda browser:\
        EC.visibility_of_element_located((By.CLASS_NAME, 'price')) \
        and visible_cars(browser, 'product-description') == reported_cars(browser))

    elems_raw = [(x.location['x'], x.location['y'], int(x.text.replace(",", ""))) for x in \
             browser.find_elements_by_class_name('price')]

    elems = [x[2] for x in sorted(elems_raw, key=lambda pos: (pos[1], pos[0]))]
    print(elems)
    assert all(a <= b  for a, b in zip(elems, elems[:1])), \
        "The list should be sorted"
