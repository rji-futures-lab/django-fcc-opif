"""
General-purpose utility functions.
"""
import re


def camelcase_to_underscore(camelcase_str):
    """
    Replace CamelCase with underscores in camelcase_str (and lower case).
    """
    underscore = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', camelcase_str)

    lower_underscore = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', underscore).lower()

    return re.sub(r'_{1,}', '_', lower_underscore)
