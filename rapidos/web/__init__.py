import os

from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap

from rapidos import Container
from rapidos.api import api, endpoints
from rapidos.config import DevelopmentConfig
from rapidos.web import views
from rapidos.web.views import RapidosView


def add_views(flask_app: Flask):
    RapidosView.register(flask_app)


def create_container(flask_app):
    container = Container()
    # noinspection PyTypeChecker
    container.wire(modules=[views, endpoints])
    flask_app.container = container


def app_api(flask_app: Flask):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    from rapidos.api.endpoints import ns
    assert ns.name == 'rapidos'
    flask_app.register_blueprint(blueprint)


def create_app():
    flask_app = Flask(__name__, template_folder='../templates', static_folder='../static')

    flask_app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

    configure_app(flask_app)
    create_container(flask_app)

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
