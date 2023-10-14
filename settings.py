import os

basedir = os.path.abspath(os.path.dirname(__file__)) + '/yacut_app'


class Config(object):
    SQLALCHEMY_DATABASE_URI = (os.getenv('TYPE_DB') +
                               os.path.join(basedir,
                                            os.getenv('NAME_DB')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
