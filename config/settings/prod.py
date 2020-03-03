"""Django settings when running project in production."""
# flake8: noqa
from boto3.session import Session
from .base import *

ALLOWED_HOSTS = [
    '.execute-api.us-east-2.amazonaws.com',
    '.rjifuture.org',
]

INSTALLED_APPS = INSTALLED_APPS + ['storages', ]

# AWS_ACCESS_KEY_ID = secrets.get('aws_access_key_id')
# AWS_SECRET_ACCESS_KEY = secrets.get('aws_secret_access_key')
AWS_S3_REGION_NAME = secrets.get('aws_region_name')
# Not sure why, but this setting is causing timeouts on the lambda.
# Works locally. Probably because of the vpc_config.
# AWS_AUTO_CREATE_BUCKET = True
AWS_BUCKET_ACL = 'public-read'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STORAGE_BUCKET_NAME = 'fcc-opif'
AWS_STATIC_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_STATIC_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

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
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# boto3_session = Session(
#     aws_access_key_id=secrets.get('aws_access_key_id'),
#     aws_secret_access_key=secrets.get('aws_secret_access_key'),
#     region_name=(AWS_S3_REGION_NAME)
# )

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#         'aws': {
#             'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'watchtower': {
#             'level': 'DEBUG',
#             'class': 'watchtower.CloudWatchLogHandler',
#                      'boto3_session': boto3_session,
#             'formatter': 'aws',
#         },
#     },
#     'loggers': {
#         'django': {
#             'level': 'INFO',
#             'handlers': ['watchtower'],
#             'propagate': False,
#         },
#     },
# }
