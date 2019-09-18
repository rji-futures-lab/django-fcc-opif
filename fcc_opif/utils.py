"""
General-purpose utility functions.
"""
import re


def camelcase_to_underscore(camelcase_str):
    """
    Replace CamelCase with underscores in camelcase_str (and lower case).
    """
    underscore = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', camelcase_str)

    lower_underscore = re.sub(
        r'([a-z0-9])([A-Z])', r'\1_\2', underscore
    ).lower()

    return re.sub(r'_{1,}', '_', lower_underscore)


def json_cleaner(data):
    new_dict = {}
    for key, value in data.items():
        if type(value) == str:
            if value.upper() == 'Y':
                value = True
            elif value.upper() == 'N':
                value = False
        new_dict[camelcase_to_underscore(key)] = value
    return new_dict
