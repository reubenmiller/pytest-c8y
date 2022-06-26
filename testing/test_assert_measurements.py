"""Assert measurement tests"""
from c8y_api.model import Device, Measurement
from pytest_c8y.device_management import DeviceManagement
import pytest


@pytest.mark.skip
def test_assert_measurement_count(sample_device: Device, device_mgmt: DeviceManagement):
    """Test measurement count"""
    device_mgmt.set_device_id(sample_device.id)

    measurement = Measurement(
        device_mgmt.c8y,
        type="cicd",
        source=sample_device.id,
        c8y_Temp={"c8y_T1": {"unit": "degC", "value": 1.23}},
    )
    device_mgmt.context.client.measurements.create()

    with pytest.raises(AssertionError):
        device_mgmt.measurements.assert_count(
            min_matches=1,
        )

    device_mgmt.measurements.assert_count(
        min_matches=1,
    )

    events = device_mgmt.measurements.assert_count(
        min_matches=1,
    )
    assert len(events) == 1
    assert events[0].id == measurement.id

    with pytest.raises(AssertionError):
        device_mgmt.measurements.assert_count(
            min_matches=1,
        )

    with pytest.raises(AssertionError):
        device_mgmt.measurements.assert_count(
            min_matches=2,
        )
