from enum import Enum

from lib.response import Component, Project, Validate

SONARCLOUD_URL = 'https://sonarcloud.io'


class SonarPlatform(Enum):
    SONARQUBE = 'sonarqube'
    SONARCLOUD = 'sonarcloud'


def from_json(json_obj):
    if 'valid' in json_obj:
        return Validate(json_obj)
    elif 'project' in json_obj:
        return Project(json_obj)
    elif 'key' in json_obj and 'name' in json_obj and 'qualifier' in json_obj:
        return Component(json_obj)
    return json_obj
