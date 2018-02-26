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
from models import Promotion, DataValidationError, db
from server import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

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
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Promotion.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_promotion(self):
        """ Create a promotion and assert that it exists """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.promotion_id, None)
        self.assertEqual(promotion.name, "20%OFF")
        self.assertEqual(promotion.product_id, 9527)

    def test_add_a_promotion(self):
        """ Create a promotion and add it to the database """
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8)
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.promotion_id, None)
        promotion.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(promotion.promotion_id, 1)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_update_a_promotion(self):
        """ Update a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8)
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Change it an save it
        promotion.category = "BUY4GET1FREE"
        promotion.save()
        self.assertEqual(promotion.promotion_id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].category, "BUY4GET1FREE")

    def test_delete_a_promotion(self):
        """ Delete a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8)
        promotion.save()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_serialize_a_promotion(self):
        """ Test serialization of a Promotion """
        promotion = Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8)
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('promotion_id', data)
        self.assertEqual(data['promotion_id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "20%OFF")
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], 9527)

    def test_deserialize_a_promotion(self):
        """ Test deserialization of a Promotion """
        data = {"promotion_id": 1, "name": "20%OFF", "product_id": 9527, "discount_ratio": 0.80}
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.promotion_id, None)
        self.assertEqual(promotion.name, "20%OFF")
        self.assertEqual(promotion.product_id, 9527)

    def test_deserialize_input_not_dict(self):
        """ Test deserialization of a Promotion with non-dict input"""
        data = [1, "20%OFF", 9527, 0.80]
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
        data = {'name': '20%OFF', 'product_id': '9527', 'discount_ratio': 0.8}
        promotion = Promotion()
        self.assertRaises(
            DataValidationError,
            promotion.deserialize,
            data)

    def test_find_promotion(self):
        """ Find a Promotion by ID """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8).save()
        black_friday_promotion = Promotion(name="50%OFF", product_id=26668)
        black_friday_promotion.save()
        promotion = Promotion.find(black_friday_promotion.promotion_id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.promotion_id, black_friday_promotion.promotion_id)
        self.assertEqual(promotion.name, "50%OFF")

    def test_find_by_category(self):
        """ Find Promotions by Product_id """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8).save()
        Promotion(name="50%OFF", product_id=26668).save()
        promotions = Promotion.find_by_product_id(9527)
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].name, "20%OFF")

    def test_find_by_name(self):
        """ Find a Promotion by Name """
        Promotion(name="20%OFF", product_id=9527, discount_ratio=0.8).save()
        Promotion(name="50%OFF", product_id=26668).save()
        promotions = Promotion.find_by_name("20%OFF")
        self.assertEqual(promotions[0].product_id, 9527)
        self.assertEqual(promotions[0].name, "20%OFF")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
