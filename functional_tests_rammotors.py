"""
Functional testing for Ram Motors
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

        # He is invited to add a new car
        # Brand, Model, year, km, cylinder, engine (fuel, diesel),
        #
        # Carrosserie: Berline Transmission:
        # Boîte manuelle Vitesses: 5 Cylindrée: 2309 cm³ Cylindres: 5
        # Poids à vide: 1370 kg Carburant: Essence
        # Portes: 4 Sièges: 5 Couleur
        # extérieure: Gris price,
        # pic features, other picture
        # options

        # <button class="btn-u" data-toggle="modal"
        # data-target="#add_vehicule" id='add_vehicule'>Add Vehicule</button>
        add_vehicule = self.browser.find_element_by_id('add_vehicule').text
        self.assertIn('Add Vehicule', add_vehicule)

        # Open a modal
        add_vehicule.send_keys(Keys.ENTER)

        input_brand = self.browser.find_element_by_id('id_new_brand')
        self.assertEqual(
            input_brand.get_attribute('placeholder'),
            'Brand'
        )

        # The user write and hit Save changes and the page list
        input_brand.send_keys('Toyota')

        """
        <div class="modal-footer">
            <button type="button" class="btn-u btn-u-default"
            data-dismiss="modal">Close</button>
            <button type="button" class="btn-u btn-u-primary"
            id='save_vehicule'>Save</button>
        </div>
        """
        add_vehicule = self.browser.find_element_by_id('save_vehicule').text
        add_vehicule.send_keys(Keys.ENTER)

        # Check that the vehicule is added to the list of vehicule
        """
      <div class="list-product-description product-description-brd
      margin-bottom-30">
       <div class="row">
        <div class="col-sm-4">
         <a href="shop-ui-inner.html"><img class="img-responsive
         sm-margin-bottom-20" src="assets/img/blog/16.jpg" alt=""></a>
        </div>
        <div class="col-sm-8 product-description">
         <div class="overflow-h margin-bottom-5">
          <ul class="list-inline overflow-h">
           <li><h4 class="title-price">
           <a href="shop-ui-inner.html"
           name='brand_list'>Toyota</a></h4></li>
           <li><span class="gender text-uppercase">Men</span></li>
           <li class="pull-right">
            <ul class="list-inline product-ratings">
             <li><i class="rating-selected fa fa-star"></i></li>
             <li><i class="rating-selected fa fa-star"></i></li>
             <li><i class="rating-selected fa fa-star"></i></li>
             <li><i class="rating fa fa-star"></i></li>
             <li><i class="rating fa fa-star"></i></li>
            </ul>
           </li>
          </ul>
          <div class="margin-bottom-10">
           <span class="title-price margin-right-10">$60.00</span>
           <span class="title-price line-through">$95.00</span>
          </div>
          <p class="margin-bottom-20">Lorem ipsum dolor sit amet,
          consectetur adipiscing elit.
          Maecenas sollicitudin erat nec ornarevolu tpat.
          Etiam ut felis nec nisl eleifend lobortis.
          Aenean nibh est, hendrerit non conva.</p>
          <ul class="list-inline add-to-wishlist margin-bottom-20">
           <li class="wishlist-in">
            <i class="fa fa-heart"></i>
            <a href="#">Add to Wishlist</a>
           </li>
           <li class="compare-in">
            <i class="fa fa-exchange"></i>
            <a href="#">Add to Compare</a>
           </li>
          </ul>
          <button type="button" class="btn-u btn-u-sea-shop">Add to Cart</button>
         </div>
        </div>
       </div>
      </div>
"""
        list_vehicules = self.browser.find_elements_by_name('brand_list')
        self.assertTrue(
            any(v.text == 'Toyota' for v in list_vehicules)
        )

        self.fail('Finish the test!')
        # He save and then he is presented with the list of already
        # saved car

if __name__ == '__main__':
    unittest.main()
