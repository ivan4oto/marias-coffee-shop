from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logger(app):
    log_level = app.config.get('LOG_LEVEL', logging.INFO)
    log_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    log_handler = RotatingFileHandler(
        'app.log', maxBytes=1024*1024*10, backupCount=5
    )
    log_handler.setLevel(log_level)
    log_handler.setFormatter(log_formatter)

    app.logger.addHandler(log_handler)
    app.logger.setLevel(log_level)


app = Flask(__name__)
configure_logger(app)

if 'APP_TESTING' in os.environ and os.environ['APP_TESTING'] == 'True':
    app.config.from_object('app.config.TestConfig')
else:
    app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import views, models
