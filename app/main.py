from __future__ import absolute_import

from flask import Flask

from configs.test import TestConfig as CONFIG

# we should only do this in one place
CONFIG.setup_services()


class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(CONFIG)

    def create_app(self):
        from .handlers.users.views import USER_BLUEPRINT
        self.app.register_blueprint(USER_BLUEPRINT)

        return self.app

