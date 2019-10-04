"""Django settings when serving locally with prod database."""
# flake8: noqa
from .prod import *
from boto3.session import Session

DEBUG = True

secrets = config['prod']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets.get('db_name'),
        'USER': secrets.get('db_user'),
        'PASSWORD': secrets.get('db_password', ''),
        'HOST': secrets.get('db_host'),
        'PORT': secrets.getint('db_port'),
    }
}

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
    '.ngrok.io',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
                     'boto3_session': boto3_session,
                     'log_group': 'MyLogGroupName',
                     'stream_name': 'MyStreamName',
        },    
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'watchtower'],
            'level': 'INFO',
        },
        'fcc_opif.management': {
            'handlers': ['console', 'watchtower'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
