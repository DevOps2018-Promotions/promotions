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
Microservice module

This module contains the microservice code for
    server
    models
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# These next lines are positional:
# 1) We need to create the Flask app
# 2) Then configure it
# 3) Then initialize SQLAlchemy after it has been configured

app = Flask(__name__)
# Load the confguration

app.config.from_object('config')
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

# Configure Swagger before initilaizing it
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "DevOps Swagger Promotion App",
            "description": "This is a sample promotion server.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ],
    "definitions": {
        "PromotionObject": {
            "type": "object",
            "required": ["discount_ratio", "name", "product_id"],
            "properties": {
                "name": {"type": "string", "example": "July4th"},
                "product_id": {"type": "integer", "example": 1785},
                "discount_ratio": {"type": "integer", "example": 75}
            },
            "example": {"product_id": 1785, "name": "July4th", "discount_ratio": 75}
        },
        "ResponsePromotionObject": {
            "type": "object",
            "required": ["counter", "discount_ratio", "name", "product_id", "promotion_id"],
            "properties": {
                "promotion_id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "July4th"},
                "product_id": {"type": "integer", "example": 1785},
                "discount_ratio": {"type": "integer", "example": 75},
                "counter": {"type": "integer", "example": 0}
            },
            "example": {
                "product_id": 1785, "name": "July4th",
                "promotion_id": 0, "counter": 0, "discount_ratio": 75
            }
        },
        "Promotion": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "July4th"},
                "product_id": {"type": "integer", "example": 1785},
                "discount_ratio": {"type": "integer"}
            },
            "example": {"product_id": 1785, "name": "July4th", "discount_ratio": 0}
        }
    }
}

# Initialize Swagger after configuring it
Swagger(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

from app import server, models
