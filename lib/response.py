def from_json(json_object) :
    if 'valid' in json_object :
        return Validate(json_object)
    return json_object


class Validate:
    def __init__(self, attrs) :
        self.valid = attrs['valid']