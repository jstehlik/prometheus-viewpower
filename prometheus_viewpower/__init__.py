import json
import os
import sys
import logging

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, REGISTRY
from prometheus_viewpower import collector


def create_app():
    app = Flask(__name__)
    app.app_context().push()

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    config_path = os.environ.get('PROMETHEUS_VIEWPOWER_CONFIGFILE') or 'config.json'
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except IOError:
        print('Failed opening config.json')
        sys.exit(4)

    REGISTRY.register(collector.ViewPowerCollector(config))

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    return app
