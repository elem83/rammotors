"""
Functional testing for Ram Motors
"""

import unittest
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

class NewAdminTest(unittest.TestCase):
    """Testing the ability to add a vehicule and to
    check it in the list of vehicule"""

    def setUp(self):
        """ Docstring """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        """ Docstring """
        self.browser.quit()

    def test_can_add_vehicule_check(self):
        """ Docstring """
        self.browser.get('http://localhost:8000/')

        # The Customer check that the title refer to his company
        assert 'Ram Motors' in self.browser.title,\
        'Browse title was: ' + self.browser.title

        # The user is happy because the developer did not need
        # any input from him.  All the cars are retrieved from
        # the websites through wsdl.
        # He goes to the site and check that all the cars are there

        self.fail('Finish the test!')
        # He save and then he is presented with the list of already
        # saved car

if __name__ == '__main__':
    unittest.main()
