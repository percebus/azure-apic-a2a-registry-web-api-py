"""Flask App."""

import logging

from flask import Flask

from a2a_registry.web import health
from a2a_registry.web.api import a2a

# TODO DI
flask_api = Flask(__name__)

logger = logging.getLogger(__name__)

flask_api.register_blueprint(health.blueprint)
flask_api.register_blueprint(a2a.blueprint)
