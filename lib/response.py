""" Sonar Responses """


class SonarObject:
    """ Parent Class for all Sonar Answers """
    def __str__(self) -> str:
        description = str()
        description += f'=={self.__class__}==\n'
        for key in vars(self):
            value = getattr(self, key)
            if not isinstance(value, list):
                description += f'{key}: {value}\n'
            else:
                description += f'==={key}===\n'
                for _ in value:
                    description += value + '\n'

        return description


class Validate(SonarObject):
    """ Holder class for a Valid Authenticad Connection """
    def __init__(self, attrs):
        self.valid = attrs['valid']


class Component(SonarObject):
    """ Holder Class for Project Search Results"""
    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])


class Project(SonarObject):
    """ Holder Class for Project Generation Results """
    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])
