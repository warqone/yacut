import os


class Config(object):
    DOMAIN = 'http://localhost'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
