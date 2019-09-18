"""Django settings when running project locally."""
# flake8: noqa
import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
    '.ngrok.io',
]

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar', ]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'fcc_opif.management': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_ROOT = 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'fcc_opif', 'static'),
]

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = 'media'