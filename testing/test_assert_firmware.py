"""Firmware assertion tests"""
from c8y_api.model import ManagedObject
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.models import Firmware
import pytest


def test_assert_firmware(device_mgmt: DeviceManagement):
    """Test firmware assertions"""
    mo = ManagedObject(c8y_Firmware=Firmware(name="linux-A", version="1.0.0").__dict__)
    device_mgmt.firmware_management.assert_firmware(
        Firmware(name="linux-.+"),
        mo=mo,
    )

    device_mgmt.firmware_management.assert_firmware(
        Firmware(name="linux-A", version="1.0.0"),
        mo=mo,
    )

    device_mgmt.firmware_management.assert_firmware(
        Firmware(name="linux-A", version="^1.+"),
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.firmware_management.assert_firmware(
            Firmware(name="linux-A", version="2.0.0"),
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.firmware_management.assert_firmware(
            Firmware(name="linux-B", version="1.0.0"),
            mo=mo,
        )


def test_assert_not_firmware(device_mgmt: DeviceManagement):
    """Test negative firmware assertions"""
    mo = ManagedObject(c8y_Firmware=Firmware(name="linux-A", version="1.0.0").__dict__)

    device_mgmt.firmware_management.assert_not_firmware(
        Firmware(name="linux-A", version="2.0.0"),
        mo=mo,
    )

    device_mgmt.firmware_management.assert_not_firmware(
        Firmware(name="linux-B"),
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.firmware_management.assert_not_firmware(
            Firmware(name="linux-A", version="1.0.0"),
            mo=mo,
        )
