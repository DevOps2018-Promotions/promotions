import os
import logging
from app.vcap_services import get_database_uri

basedir = os.path.abspath(os.path.dirname(__file__))

# if 'TEST' in os.environ:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/test.db')
# else:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/development.db')

SQLALCHEMY_DATABASE_URI = get_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 500
SQLALCHEMY_POOL_RECYCLE = 300

SECRET_KEY = 'secret-for-dev-only'
LOGGING_LEVEL = logging.INFO
