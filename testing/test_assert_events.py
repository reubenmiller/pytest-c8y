"""Event assertion tests"""
from c8y_api.model import Device, Event
from c8y_test_core.device_management import DeviceManagement
import pytest


def test_assert_count(sample_device: Device, device_mgmt: DeviceManagement):
    """Test event count"""
    device_mgmt.set_device_id(sample_device.id)

    with pytest.raises(AssertionError):
        device_mgmt.events.assert_count(
            min_matches=1,
        )

    event = Event(
        device_mgmt.context.client,
        time="now",
        type="ci_cd",
        text="My test event",
        source=sample_device.id,
    ).create()

    device_mgmt.events.assert_count(
        min_matches=1,
    )

    events = device_mgmt.events.assert_count(
        expected_text="My test event",
        min_matches=1,
    )
    assert len(events) == 1
    assert events[0].id == event.id

    with pytest.raises(AssertionError):
        device_mgmt.events.assert_count(
            expected_text="^Temperature.+$",
            min_matches=1,
        )

    with pytest.raises(AssertionError):
        device_mgmt.events.assert_count(
            min_matches=2,
            expected_text=".+",
        )
