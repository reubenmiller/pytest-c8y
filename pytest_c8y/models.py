import dataclasses

from pytest_c8y.compare import compare_dataclass


@dataclasses.dataclass
class Firmware:
    name: str = ""
    version: str = ""
    url: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(self, obj)


@dataclasses.dataclass
class Software:
    name: str = ""
    version: str = ""
    url: str = ""
    action: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(self, obj)


@dataclasses.dataclass
class Configuration:
    type: str = ""
    url: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(self, obj)
