class SonarObject:
    def __str__(self) -> str:
        description = str()
        description += f'=={self.__class__}==\n'
        for key in vars(self):
            value = getattr(self, key)
            if not isinstance(value, list):
                description += '{}: {}\n'.format(key, value)
            else:
                description += f'==={key}===\n'
                for _ in value:
                    description += value + '\n'

        return description


class Validate(SonarObject):
    def __init__(self, attrs):
        self.valid = attrs['valid']


class Component(SonarObject):
    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])


class Project(SonarObject):
    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])
