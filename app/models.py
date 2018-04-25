# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for Promotion Service

All of the models are stored in this module

Models
------
Promotion - A Promotion used in the eCommerce Site

Attributes:
-----------
promotion_id (integer) - the id of the promotion
name (string) - the name of the promotion
product_id (integer) - the id of the product associated with the promotion
discount_ratio (float) - the discount ratio
"""
import logging
import threading
from flask_sqlalchemy import SQLAlchemy
from . import db

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Promotion(db.Model):
    """
    Class that represents a Promotion

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)

    # Table Schema
    promotion_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    product_id = db.Column(db.Integer)
    discount_ratio = db.Column(db.Integer)
    counter = db.Column(db.Integer)
    # start_date = db.Column(db.DateTime)
    # end_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Promotion %r, %r, %r>' % (self.name, self.product_id, self.discount_ratio)

    def save(self):
        """
        Saves a Promotion to the data store
        """
        if not self.promotion_id:
            self.counter = 0
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Promotion from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Promotion into a dictionary """
        return {"promotion_id": self.promotion_id,
                "name": self.name,
                "product_id": self.product_id,
                "discount_ratio": self.discount_ratio,
                "counter": self.counter}

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the Promotion data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid promotion: body of request contained bad or no data')
        try:
            new_name = "" + data['name']
            new_product_id = 0 + data['product_id']
            new_discount_ratio = 0 + data['discount_ratio']
            if new_discount_ratio < 0 or new_discount_ratio > 100:
                raise DataValidationError('Invalid promotion: discount_ratio out of range'\
                                          'expecting value between 0 to 100')
            self.name = new_name
            self.product_id = new_product_id
            self.discount_ratio = new_discount_ratio
            # self.start_date = data['start_date']
            # self.end_date = data['end_date']
        except KeyError as error:
            raise DataValidationError('Invalid promotion: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid promotion: body of request contained' \
                                      'bad or no data')
        return self

    def deserialize_partial(self, data):
        """
        Deserializes a partial Promotion from a dictionary, only used for partial update

        Args:
            data (dict): A dictionary containing the partial Promotion data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid promotion: body of request contained bad or no data')
        try:
            count = 0
            if 'name' in data:
                new_name = "" + data['name']
                count = count + 1
            if 'product_id' in data:
                new_product_id = 0 + data['product_id']
                count = count + 1

            if 'discount_ratio' in data:
                new_discount_ratio = 0 + data['discount_ratio']
                if new_discount_ratio < 0 or new_discount_ratio > 100:
                    raise DataValidationError('Invalid promotion: discount_ratio out of range'\
                                          'expecting value between 0 to 100')
                count = count + 1

            if count == 0:
                raise DataValidationError('Invalid promotion: missing update data')

            if 'name' in data:
                self.name = new_name
            if 'product_id' in data:
                self.product_id = new_product_id
            if 'discount_ratio' in data:
                self.discount_ratio = new_discount_ratio

        except TypeError as error:
            raise DataValidationError('Invalid promotion: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def remove_all():
        db.drop_all()
        db.create_all()

    @staticmethod
    def init_db():
        """ Initializes the database session """
        Promotion.logger.info('Initializing database')
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Returns all of the Promotions in the database """
        Promotion.logger.info('Processing all Promotions')
        return Promotion.query.all()

    @staticmethod
    def find(promotion_id):
        """ Finds a Promotions by it's ID """
        if not isinstance(promotion_id, int):
            raise DataValidationError('Invalid promotion: body of request contained bad or no data')
        Promotion.logger.info('Processing lookup for id %s ...', promotion_id)
        return Promotion.query.get(promotion_id)

    @staticmethod
    def find_or_404(promotion_id):
        """ Find a promotion_id by it's id """
        Promotion.logger.info('Processing lookup or 404 for id %s ...', promotion_id)
        return Promotion.query.get_or_404(promotion_id)

    @staticmethod
    def find_by_name(name):
        """ Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        Promotion.logger.info('Processing name query for %s ...', name)
        return Promotion.query.filter(Promotion.name == name)

    @staticmethod
    def find_by_product_id(product_id):
        """ Returns all Promotions of a specific product

        Args:
            product_id (Integer): product id of the Promotions you want to match
        """
        Promotion.logger.info('Processing product_id query for %s ...', product_id)
        return Promotion.query.filter(Promotion.product_id == product_id)

    @staticmethod
    def find_by_discount_ratio(discount_ratio):
        """ Returns all Promotions of a specific product

        Args:
            discount_ratio (Float): product id of the Promotions you want to match
        """
        Promotion.logger.info('Processing product_id query for %r ...', discount_ratio)
        return Promotion.query.filter(Promotion.discount_ratio == discount_ratio)

    @staticmethod
    def redeem_promotion(promotion_id):
        """ Redeem a Promotions by it's ID. Thread Safe. """
        if not isinstance(promotion_id, int):
            raise DataValidationError('Invalid promotion: body of request contained bad or no data')
        Promotion.logger.info('Redeem promotion %s ...', promotion_id)
        # If the promotion doesn't exist, 404 will be raised.
        promotion = Promotion.find_or_404(promotion_id)
        promotion.counter = promotion.counter + 1
        db.session.commit()
        return promotion
