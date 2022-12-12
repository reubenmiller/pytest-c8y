"""Test firmware"""

import re
from c8y_test_core.models import Firmware


def test_firmware_comparison():
    """Test firmware version comparison"""
    firmware = Firmware(name="linuxA", version="1.0.1")

    assert firmware == {"name": "linuxA", "version": "1.0.1"}
    assert firmware == Firmware(name="linuxA", version="1.0.1")
    assert firmware != Firmware(
        name="linuxA",
        version="1.0.2",
    )
    assert firmware != Firmware(name="linuxA", version="1.0.1", url="test")
    assert firmware == Firmware(name="linuxA", version=re.compile(".+"))
    assert firmware != Firmware(name="linuxA", version=re.compile(".+"), url=re.compile(".+"))
