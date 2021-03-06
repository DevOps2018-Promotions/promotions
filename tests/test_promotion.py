# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Promotion Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app import app, db
from app.models import Promotion, DataValidationError

# DATABASE_URI = 'mysql+pymysql://root:passw0rd@localhost:3306/test'
DATABASE_URI = os.getenv('DATABASE_URI', None)
######################################################################
#  T E S T   C A S E S
######################################################################


class TestPromotions(unittest.TestCase):
    """ Test Cases for Promotions """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        if DATABASE_URI:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_promotion(self):
        """ Create a promotion and assert that it exists """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.promotion_id, None)
        self.assertEqual(promotion.name, "20%OFF")
        self.assertEqual(promotion.product_id, 9527)
        self.assertIsNone(promotion.counter)

    def test_add_a_promotion(self):
        """ Create a promotion and add it to the database """
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.promotion_id, None)
        promotion.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(promotion.promotion_id, 1)
        self.assertEqual(promotion.counter, 0)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_update_a_promotion(self):
        """ Update a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Change it an save it
        promotion.name = "BUY1GET1FREE"
        promotion.product_id = 9528
        promotion.discount_ratio = 50
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].name, "BUY1GET1FREE")
        self.assertEqual(promotions[0].product_id, 9528)
        self.assertEqual(promotions[0].discount_ratio, 50)

    def test_partial_update_an_promotion(self):
        """ Partial update a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Change it an save it
        promotion.name = "BUY1GET1FREE"
        promotion.discount_ratio = 50
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].name, "BUY1GET1FREE")
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].discount_ratio, 50)

    def test_delete_a_promotion(self):
        """ Delete a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        promotion.save()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_serialize_a_promotion(self):
        """ Test serialization of a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=80)
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('promotion_id', data)
        self.assertEqual(data['promotion_id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "20%OFF")
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], 9527)
        self.assertIn('counter', data)
        self.assertIsNone(data['counter'])
        self.assertIn('discount_ratio', data)
        self.assertEqual(data['discount_ratio'], 80)

    def test_deserialize_a_promotion(self):
        """ Test deserialization of a Promotion """
        data = {"promotion_id": 1, "name": "20%OFF", "product_id": 9527, "discount_ratio": 80}
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.promotion_id, None)
        self.assertEqual(promotion.name, "20%OFF")
        self.assertEqual(promotion.product_id, 9527)
        self.assertEqual(promotion.discount_ratio, 80)

    def test_deserialize_input_not_dict(self):
        """ Test deserialization of a Promotion with non-dict input"""
        data = [1, "20%OFF", 9527, 80]
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_deserialize_key_error(self):
        """ Test deserialization of a Promotion with KeyError input"""
        data = {}
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_deserialize_type_error(self):
        """ Test deserialization of a Promotion with TypeError input"""
        data = {'name': '20%OFF', 'product_id': '9527', 'discount_ratio': 80}
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_deserialize_value_too_low(self):
        """ Test deserialization of a Promotion with input value too low"""
        data = {'name': '20%OFF', 'product_id': 9527, 'discount_ratio': -1}
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_deserialize_value_too_high(self):
        """ Test deserialization of a Promotion with input value out of range"""
        data = {'name': '20%OFF', 'product_id': 9527, 'discount_ratio': 200}
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_find_promotion(self):
        """ Find a Promotion by ID """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        black_friday_promotion = Promotion(name="50%OFF", product_id=26668)
        black_friday_promotion.save()
        promotion = Promotion.find(black_friday_promotion.promotion_id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.promotion_id, black_friday_promotion.promotion_id)
        self.assertEqual(promotion.name, "50%OFF")

    def test_find_promotion_input_nonexistent_id(self):
        """ Test find promotion function with nonexistent ID """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        promotion = Promotion.find(2)
        self.assertEqual(promotion, None)

    def test_find_promotion_input_not_id(self):
        """ Test find promotion function with invalid ID type"""
        data = "a"
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.find,
            data
        )

    def test_find_by_product_id(self):
        """ Find Promotions by Product_id """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        Promotion(name="50%OFF", product_id=26668).save()
        promotions = Promotion.find_by_product_id(9527)
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].name, "20%OFF")

    def test_find_by_name(self):
        """ Find a Promotion by Name """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        Promotion(name="50%OFF", product_id=26668).save()
        promotions = Promotion.find_by_name("20%OFF")
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].name, "20%OFF")

    def test_find_or_404(self):
        """ Find promotion or 404 """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        promotion = Promotion.find_or_404(1)
        self.assertIsNotNone(promotion)
        self.assertEqual(promotion.promotion_id, 1)
        self.assertEqual(promotion.name, "20%OFF")
        self.assertEqual(promotion.product_id, 9527)
        self.assertEqual(promotion.discount_ratio, 80)
        self.assertEqual(promotion.counter, 0)

    def test_find_or_404_404(self):
        """ Find promotion or 404 expecting 404 """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        try:
            promotion = Promotion.find_or_404(2)
            # Should not reach beyond this line.
            self.assertIsNone(promotion)
        except:
            pass

    def test_find_by_discount_ratio(self):
        """ Find a Promotion by Discount ratio """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        Promotion(name="50%OFF", product_id=26668).save()
        promotions = Promotion.find_by_discount_ratio(80)
        Promotion.logger.info(promotions)
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].name, "20%OFF")

    def test_redeem_promotion(self):
        """ Redeem a Promoion """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        promotion = Promotion.find(1)
        self.assertEqual(promotion.counter, 0)
        Promotion.redeem_promotion(1)
        self.assertEqual(promotion.counter, 1)
        Promotion.redeem_promotion(1)
        self.assertEqual(promotion.counter, 2)

    def test_redeem_promotion_bad_data(self):
        """ Redeem a Promoion with bad data """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        self.assertRaises(DataValidationError, Promotion.redeem_promotion, "a")

    def test_remove_all(self):
        """ Remove all entries """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=80).save()
        Promotion(name="50%OFF", product_id=26668).save()
        Promotion.remove_all()
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 0)
######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
