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
Promotion Service Runner

Start the Promotion Service and initializes logging
"""

import os
from app import app, server

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "************************************************************"
    print "    P R O M O T I O N   R E S T   A P I   S E R V I C E     "
    print "************************************************************"
    server.initialize_logging()
    server.init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
