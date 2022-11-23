from flask import Flask, g, render_template, request, redirect
import logging
import time

from app import config
from app.extensions import migrate, bcrypt, lm
from app.data import db
from app.assets import assets
from app.public import public
from app.auth import auth
from app.admin import admin


def create_app(config=config.base_config):
    app = Flask(__name__)
    app.config.from_object(config)

    logger = logging.getLogger()
    formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler = logging.FileHandler(config.LOG_FILEPATH, encoding='utf-8')
    file_handler.setLevel(config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # app.logger.addHandler(file_handler)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    #register_jinja_env(app)

    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: f'{time.time() - g.request_start_time:.5f}s'
    
    @app.template_filter()
    def format_datetime(value, format='%Y/%m/%d %H:%M'):
        return value.strftime(format)

    @app.route('/forceerror')
    def force_error():
        return 1/0

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    lm.init_app(app)
    assets.init_app(app)


def register_blueprints(app):
    app.register_blueprint(public)
    app.register_blueprint(auth)
    app.register_blueprint(admin)


def register_errorhandlers(app):
    def render_error(e):
        code = e.code if hasattr(e, "code") else 500
        if code==500:
            app.logger.error(e)
        else:
            app.logger.info(e)
        return f'Error {code}', code
        # return render_template('errors/%s.html' % code), code

    for e in [401, 404, 500]:
        app.errorhandler(e)(render_error)

