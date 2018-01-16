# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in __init__.py
"""


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()

from flask_migrate import Migrate
migrate = Migrate()
