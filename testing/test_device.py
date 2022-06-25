from c8y_api.model import Device
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.models import Software
import pytest

pytestmark = pytest.mark.nondestructive


def test_sample_device(sample_device: Device):
    """Create a sample device"""
    assert sample_device.id


def test_software_management_install(
    sample_device: Device, device_mgmt: DeviceManagement
):
    assert sample_device.id
    device_mgmt.set_device_id(sample_device.id)

    operation = device_mgmt.software_management.install(
        Software(name="test", version="1.0.0", action="install")
    )
    operation.assert_failed()
