import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:mypassword@localhost:5432/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://mytestuser:mytestpassword@localhost:5432/mytestdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False