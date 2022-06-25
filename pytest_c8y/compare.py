import re


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern


class pytest_softwarelist:
    """Assert that a given string meets some expectations."""

    def __init__(self, software_list):
        self._software_list = software_list

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern


def compare_dataclass(obj1: object, obj2: object) -> bool:
    obj2_dict = obj2.__dict__ if not isinstance(obj2, dict) else obj2
    for key, value in obj2_dict.items():
        if not hasattr(obj1, key):
            return False

        if not re.match(value, getattr(obj1, key)):
            return False
    return True
