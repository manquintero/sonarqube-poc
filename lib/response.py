def from_json(json_obj):
    if 'valid' in json_obj:
        return Validate(json_obj)
    elif 'key' in json_obj and 'name' in json_obj and 'qualifier' in json_obj:
        if 'revision' in json_obj:
            return Component(json_obj)
        else:
            return Project(json_obj)
    return json_obj


class Validate:
    def __init__(self, attrs):
        self.valid = attrs['valid']


class Component:
    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])


class Project:

    def __init__(self, attrs):
        for key in attrs:
            setattr(self, key, attrs[key])