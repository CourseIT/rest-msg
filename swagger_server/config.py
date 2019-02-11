# coding: utf-8
# pylint: disable=invalid-name, missing-docstring
import logging.config
import os

import connexion
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from jinja2 import Environment, BaseLoader

load_dotenv(find_dotenv())
BASEDIR = os.path.dirname(__file__)


class Config(object):
    """Base class for app configuration"""
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    AUTHORIZATION = os.getenv('AUTHORIZATION')

    APP_PORT = os.getenv('APP_PORT', '8000')

    MSG_TEMPLATE = Environment(loader=BaseLoader).from_string("""ВНИМАНИЕ!
    C {{ banner.date_start.strftime('%H:%M %d.%m.%Y') }}
    до {{ banner.date_finish.strftime('%H:%M %d.%m.%Y') }} на серверах системы
    будут проводиться регламентные профилактические работы,
    в связи с чем система будет недоступна.
    Приносим извинения за неудобства и надеемся на понимание.""")

    @property
    def LOGGING_CONFIG(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format':
                        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': self.LOG_LEVEL,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler'
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': self.LOG_LEVEL,
                    'propagate': True
                }
            }
        }

    def __init__(self):
        self.BASEDIR = BASEDIR
        logging.config.dictConfig(self.LOGGING_CONFIG)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False

    @property
    def LOGGING_CONFIG(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format':
                        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': self.LOG_LEVEL,
                    'formatter': 'standard',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(BASEDIR, 'logs', 'bot.log'),
                    'mode': 'a',
                    'maxBytes': 1 << 20,  # 1M
                    'backupCount': 5,
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': self.LOG_LEVEL,
                    'propagate': True
                }
            }
        }


# При инициализации бота должно указываться название запускаемой конфигурации,
#   либо по умолчанию будет режим dev
_config_relation = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

ConfigClass = _config_relation[os.environ.get('CONFIG', 'default')]
settings = ConfigClass()

app = connexion.App(__name__, specification_dir='./swagger/')

# Configure the SqlAlchemy part of the app instance
app.app.config.from_object(settings)

# Create the SqlAlchemy db instance
db = SQLAlchemy(app.app)
CORS(app.app)
