"""Models"""
import dataclasses

from pytest_c8y.compare import compare_dataclass


@dataclasses.dataclass
class Firmware:
    """Firmware"""

    name: str = ""
    version: str = ""
    url: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(obj, self)


@dataclasses.dataclass
class Software:
    """Software"""

    name: str = ""
    version: str = ""
    url: str = ""
    action: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(obj, self)


@dataclasses.dataclass
class Configuration:
    """Configuration"""

    type: str = ""
    url: str = ""

    def __eq__(self, obj: object) -> bool:
        return compare_dataclass(self, obj)
