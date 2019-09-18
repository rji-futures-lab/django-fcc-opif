"""Django settings when running project in test environment."""
# flake8: noqa
from .local import * # noqa

THROTTLE_TWITTER_API_CALLS = False

LOGGING = {}
