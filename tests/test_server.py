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
Promotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""


import unittest
import os
import json
import logging
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch
import threading

from app.models import Promotion, DataValidationError
from app import server, db

# DATABASE_URI = 'mysql+pymysql://root:passw0rd@localhost:3306/test'
DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################


class TestPromotionServer(unittest.TestCase):
    """ Promotion Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.INFO)
        # Set up the test database
        if DATABASE_URI:
            server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        Promotion(name='20%OFF', product_id=9527, discount_ratio=80).save()
        Promotion(name='50%OFF', product_id=26668, discount_ratio=50).save()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Promotion RESTful API Service')

    def test_get_promotion_list(self):
        """ Get a list of Promotions """
        resp = self.app.get('/promotions')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_promotion(self):
        """ Get a single Promotion """
        # get the promotion_id of a promotion
        promotion = Promotion.find_by_name('20%OFF')[0]
        resp = self.app.get('/promotions/{}'.format(promotion.promotion_id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], promotion.name)

    def test_get_promotion_not_found(self):
        """ Get a Promotion thats not found """
        resp = self.app.get('/promotions/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_promotion_wrong_id_type(self):
        """ Get a Promotion with wrong id type """
        resp = self.app.get('/promotions/a')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_promotion(self):
        """ Create a new Promotion """
        # save the current number of promotions for later comparison
        promotion_count = self.get_promotion_count()
        # add a new promotion
        new_promotion = {'name': 'ALLFREE', 'product_id': 1982, 'discount_ratio':0}
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'ALLFREE')
        # check that count has gone up and includes sammy
        resp = self.app.get('/promotions')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), promotion_count + 1)
        self.assertIn(new_json, data)

    def test_create_wrong_content_type(self):
        promotion_count = self.get_promotion_count()
        # add a new promotion
        new_promotion = "{'name': 'ALLFREE', 'product_id': 1982, 'discount_ratio':0}"
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data, content_type='text/plain')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_bad_request(self):
        promotion_count = self.get_promotion_count()
        # add a new promotion
        new_promotion = {'name': 'ALLFREE', 'product_id': '1982', 'discount_ratio': 0}
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_promotion(self):
        """ Update an existing Promotion """
        promotion_count = self.get_promotion_count()
        promotion = Promotion.find_by_name('50%OFF')[0]
        promotion_id = promotion.promotion_id
        new_promotion = {'name': '90%OFF', 'product_id': 2609, 'discount_ratio': 10}
        data = json.dumps(new_promotion)
        resp = self.app.put('/promotions/{}'.format(promotion_id), data=data,
                            content_type='application/json')
        new_promotion_count = self.get_promotion_count()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(promotion_count, new_promotion_count)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['promotion_id'], promotion_id)
        self.assertEqual(new_json['name'], '90%OFF')
        self.assertEqual(new_json['product_id'], 2609)
        self.assertEqual(new_json['discount_ratio'], 10)

    def test_update_promotion_promotion_id_not_found(self):
        """ Update a non-existing Promotion """
        promotion_count = self.get_promotion_count()
        promotion_id = 999
        new_promotion = {'name': '90%OFF', 'product_id': 2609, 'discount_ratio': 10}
        data = json.dumps(new_promotion)
        resp = self.app.put('/promotions/{}'.format(promotion_id), data=data,
                            content_type='application/json')
        new_promotion_count = self.get_promotion_count()
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(promotion_count, new_promotion_count)

    def test_update_promotion_wrong_content_type(self):
        """ Update an existing Promotion with wrong input format"""
        promotion_count = self.get_promotion_count()
        promotion = Promotion.find_by_name('50%OFF')[0]
        promotion_id = promotion.promotion_id
        new_promotion = "{'name': '90%OFF', 'product_id': 2609, 'discount_ratio': 10}"
        data = json.dumps(new_promotion)
        resp = self.app.put('/promotions/{}'.format(promotion_id), data=data,
                            content_type='application/plain')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        new_promotion_count = self.get_promotion_count()
        self.assertEqual(promotion_count, new_promotion_count)
        self.assertEqual(promotion.name, "50%OFF")
        self.assertEqual(promotion.product_id, 26668)
        self.assertEqual(promotion.discount_ratio, 50)

    def test_update_promotion_bad_request_wrong_value_type(self):
        """ Update an existing Promotion with wrong data type"""
        promotion_count = self.get_promotion_count()
        promotion = Promotion.find_by_name('50%OFF')[0]
        promotion_id = promotion.promotion_id
        new_promotion = {'name': '90%OFF', 'product_id': '2609', 'discount_ratio': 10}
        data = json.dumps(new_promotion)
        resp = self.app.put('/promotions/{}'.format(promotion_id), data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        new_promotion_count = self.get_promotion_count()
        self.assertEqual(promotion_count, new_promotion_count)
        self.assertEqual(promotion.name, "50%OFF")
        self.assertEqual(promotion.product_id, 26668)
        self.assertEqual(promotion.discount_ratio, 50)

    def test_update_promotion_bad_request_value_out_of_range(self):
        """ Update an existing Promotion with wrong value"""
        promotion_count = self.get_promotion_count()
        promotion = Promotion.find_by_name('50%OFF')[0]
        promotion_id = promotion.promotion_id
        new_promotion = {'name': '90%OFF', 'product_id': 2609, 'discount_ratio': 200}
        data = json.dumps(new_promotion)
        resp = self.app.put('/promotions/{}'.format(promotion_id), data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        new_promotion_count = self.get_promotion_count()
        self.assertEqual(promotion_count, new_promotion_count)
        self.assertEqual(promotion.name, "50%OFF")
        self.assertEqual(promotion.product_id, 26668)
        self.assertEqual(promotion.discount_ratio, 50)

    def test_delete_promotion(self):
        """ Delete a Promotion """
        promotion = Promotion.find_by_name('20%OFF')[0]
        # save the current number of promotions for later comparison
        promotion_count = self.get_promotion_count()
        resp = self.app.delete('/promotions/{}'.format(promotion.promotion_id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_promotion_count()
        self.assertEqual(new_count, promotion_count - 1)

    def test_delete_promotion_not_found(self):
        """ Delete a Promotion thats not found """
        # save the current number of promotions for later comparison
        promotion_count = self.get_promotion_count()
        resp = self.app.delete('/promotions/{}'.format(0),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        new_count = self.get_promotion_count()
        self.assertEqual(new_count, promotion_count)

    def test_delete_promotion_wrong_id_type(self):
        """ Delete a Promotion with wrong id type """
        # save the current number of promotions for later comparison
        promotion_count = self.get_promotion_count()
        resp = self.app.delete('/promotions/{}'.format("a"),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        new_count = self.get_promotion_count()
        self.assertEqual(new_count, promotion_count)

    def test_query_promotion_list_by_name(self):
        """ Query Promotions by Name """
        resp = self.app.get('/promotions', query_string='name=20%OFF')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('20%OFF', resp.data)
        self.assertNotIn('50%OFF', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['product_id'], 9527)

    def test_query_promotion_list_by_product_id(self):
        """ Query Promotions by Product id """
        resp = self.app.get('/promotions', query_string='product_id=9527')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('9527', resp.data)
        self.assertNotIn('9526', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['name'], '20%OFF')

    def test_query_promotion_list_by_discount_ratio(self):
        """ Query Promotions by Discount ratio """
        resp = self.app.get('/promotions', query_string='discount_ratio=80')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)
        query_item = data[0]
        self.assertEqual(80, query_item['discount_ratio'])
        self.assertEqual(query_item['product_id'], 9527)

    def test_redeem_promotions(self):
        """ Redeem a promotion """
        for i in xrange(1, 20):
            promotion = Promotion.find_by_name('50%OFF')[0]
            resp = self.app.post('/promotions/{}/redeem'.format(promotion.promotion_id))
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            resp = self.app.get('/promotions/{}'.format(promotion.promotion_id))
            new_json = json.loads(resp.data)
            self.assertEqual(new_json['counter'], i)

    def test_redeem_promotions_not_fount(self):
        """ Redeem a promotion with invalid id """
        resp = self.app.post('/promotions/3/redeem')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_redeem_promotions_method_not_suported(self):
        """ Redeem a promotion with the wrong method """
        promotion = Promotion.find_by_name('50%OFF')[0]
        resp = self.app.post('/promotions/{}/redeem'.format(promotion.promotion_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/promotions/{}/redeem'.format(promotion.promotion_id))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.app.put('/promotions/{}/redeem'.format(promotion.promotion_id))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.app.delete('/promotions/{}/redeem'.format(promotion.promotion_id))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('app.server.Promotion.find_by_name')
    def test_bad_request(self, bad_request_mock):
        """ Test a Bad Request error from Find By Name """
        bad_request_mock.side_effect = DataValidationError()
        resp = self.app.get('/promotions', query_string='name=20%OFF')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.server.Promotion.find_by_name')
    def test_mock_search_data(self, promotion_find_mock):
        """ Test showing how to mock data """
        promotion_find_mock.return_value = [MagicMock(serialize=lambda: {'name': '20%OFF'})]
        resp = self.app.get('/promotions', query_string='name=20%OFF')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
# Utility functions
######################################################################

    def get_promotion_count(self):
        """ save the current number of promotions """
        resp = self.app.get('/promotions')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
