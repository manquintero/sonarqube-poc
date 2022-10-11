""" Sonar Responses """


class SonarObject:
    """ Parent Class for all Sonar Answers """
    def __str__(self) -> str:
        description = str()
        description += f'=={self.__class__}==\n'
        for key in vars(self):
            value = getattr(self, key)
            description += f'{key}: {value}\n'

        return description


class Validate(SonarObject):
    """ Holder class for a Valid Authenticad Connection """
    def __init__(self, attrs):
        self.valid = attrs['valid']


class Component(SonarObject):
    """ Holder Class for Project Search Results"""
    def __init__(self, attrs):
        # Primitives
        self.organization = None
        self.key = None
        self.name = None
        self.qualifier = None
        self.visibility = None
        self.lastAnalysisDate = None
        self.revision = None

        for key in attrs:
            setattr(self, key, attrs[key])


class Branch(SonarObject):
    """ Holder Class for Branch in a Project """

    def __init__(self, attrs):
        self.name = None
        self.isMain = None
        self.type = None
        self.mergeBranch = None
        self.status = None
        self.analysisDate = None
        self.commit = None

        for key in attrs:
            setattr(self, key, attrs[key])
