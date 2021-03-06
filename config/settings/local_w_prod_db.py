"""Django settings when serving locally with prod database."""
# flake8: noqa
from .local import *

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
