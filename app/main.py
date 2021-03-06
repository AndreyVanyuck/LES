from __future__ import absolute_import

from flask import Flask

from configs.run_config import CONFIG

# we should only do this in one place
CONFIG.setup_services()


class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(CONFIG)

    def create_app(self):
        from .handlers.users.views import USERS_BLUEPRINT
        from .handlers.departments.views import DEPARTMENTS_BLUEPRINT
        from .handlers.rooms.views import ROOMS_BLUEPRINT
        from .handlers.buildings.views import BUILDINGS_BLUEPRINT
        from .handlers.requests.views import REQUESTS_BLUEPRINT

        self.app.register_blueprint(USERS_BLUEPRINT)
        self.app.register_blueprint(DEPARTMENTS_BLUEPRINT)
        self.app.register_blueprint(ROOMS_BLUEPRINT)
        self.app.register_blueprint(BUILDINGS_BLUEPRINT)
        self.app.register_blueprint(REQUESTS_BLUEPRINT)

        return self.app
