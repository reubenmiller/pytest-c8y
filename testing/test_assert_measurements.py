"""Assert measurement tests"""
from c8y_api.model import Device, Measurement
from c8y_test_core.device_management import DeviceManagement
import pytest


def test_assert_measurement_count(sample_device: Device, device_mgmt: DeviceManagement):
    """Test measurement count"""
    device_mgmt.set_device_id(sample_device.id)

    measurement = Measurement(
        device_mgmt.c8y,
        type="cicd",
        source=sample_device.id,
        c8y_Temp={"c8y_T1": {"unit": "degC", "value": 1.23}},
    ).create()

    with pytest.raises(AssertionError):
        device_mgmt.measurements.assert_count(
            min_count=2,
        )

    measurements = device_mgmt.measurements.assert_count(
        min_count=1,
        type="cicd",
    )

    assert len(measurements) == 1
    assert measurements[0].id == measurement.id

    with pytest.raises(AssertionError):
        device_mgmt.measurements.assert_count(
            min_count=1,
            type="cicd_invalid",
        )
