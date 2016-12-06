"""
Functional testing for Ram Motors
"""

import unittest
from selenium import webdriver

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
        self.browser.get('http://localhost:8000/vehicules')

        # The Customer check that the title refer to his company
        assert 'Vehicules' in self.browser.title,\
        'Browse title was: ' + self.browser.title

        self.fail('Finish the test!')
        # He is invited to add a new car
        # Brand, Model, year, km, pic features, other picture

        # He save and then he is presented with the list of already
        # saved car

if __name__ == '__main__':
    unittest.main()
