from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
if 'APP_TESTING' in os.environ and os.environ['APP_TESTING'] == 'True':
    app.config.from_object('app.config.TestConfig')
else:
    app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models
