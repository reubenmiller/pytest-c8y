from dataclasses import dataclass
import logging
from c8y_api import CumulocityApi


@dataclass
class AssertContext:
    device_id: str = ""
    client: CumulocityApi = None
    log: logging.Logger = None
