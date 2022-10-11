""" Sonar Utilities"""
from enum import Enum


from lib.response import Component, Validate, Branch
SONARCLOUD_URL = 'https://sonarcloud.io'


class SonarPlatform(Enum):
    """ Enumeration for Types of supported Platforms """
    SONARQUBE = 'sonarqube'
    SONARCLOUD = 'sonarcloud'


def from_json(json_obj):
    """ Callback for transforming Sonar JSON responses into Objects"""
    if 'valid' in json_obj:
        return Validate(json_obj)
    if 'isMain' in json_obj:
        return Branch(json_obj)
    if 'key' in json_obj and 'name' in json_obj and 'qualifier' in json_obj:
        return Component(json_obj)
    return json_obj


