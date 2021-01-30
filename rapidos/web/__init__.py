import os

from flask import Flask
from flask_bootstrap import Bootstrap

from rapidos import Container
from rapidos.config import DevelopmentConfig
from rapidos.web import views
from rapidos.web.views import CreateView
from rapidos.web.views import MarketplaceView


def add_views(flask_app: Flask):
    flask_app.container = create_container()
    CreateView.register(flask_app)
    MarketplaceView.register(flask_app)


def create_container():
    container = Container()
    # noinspection PyTypeChecker
    container.wire(modules=[views])
    return container


def app_api(flask_app: Flask):
    pass


def create_app():
    flask_app = Flask(__name__, template_folder='../templates', static_folder='../static')

    flask_app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

    configure_app(flask_app)
    add_views(flask_app)

    app_api(flask_app)

    Bootstrap(flask_app)

    return flask_app


def configure_app(flask_app):
    app_config = {
        'default': DevelopmentConfig.config_string()
    }
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    flask_app.config.from_object(app_config[config_name])
