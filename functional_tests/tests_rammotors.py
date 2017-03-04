# pylint: disable=unused-argument, redefined-outer-name, missing-docstring
"""
Functional testing for Ram Motors
"""

import pytest

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

@pytest.fixture(scope="module")
def browser(request):
    selenium = webdriver.Firefox()
    selenium.implicitly_wait(3)
    def teardown():
        selenium.quit()
    request.addfinalizer(teardown)
    return selenium

def test_browsing_check(browser):
    """ Docstring """
    browser.get('http://localhost:8000')

    # Checking that title is right
    assert 'Ram Motors' in browser.title,\
    'Browse title was: ' + browser.title
