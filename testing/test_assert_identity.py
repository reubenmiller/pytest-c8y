"""Identity assertion tests"""
from c8y_api.model import ManagedObject, Device
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.utils import RandomNameGenerator
import pytest


def test_identity_exists(sample_device: Device, device_mgmt: DeviceManagement):
    """Test identity exists"""
    external_id = RandomNameGenerator.random_name()
    external_type = "CI_CD"

    with pytest.raises(AssertionError):
        device_mgmt.identity.assert_exists(
            external_id=external_id,
            external_type=external_type,
        )

    device_mgmt.context.client.identity.create(
        external_id, external_type, sample_device.id
    )
    mo = device_mgmt.identity.assert_exists(
        external_id=external_id,
        external_type=external_type,
    )
    assert mo.id == sample_device.id
