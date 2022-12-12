"""Device availability/connectivity assertion tests"""
from c8y_api.model import ManagedObject
from c8y_test_core.device_management import DeviceManagement
import pytest


def test_assert_connection(device_mgmt: DeviceManagement):
    """Test device connection assertions"""
    mo = ManagedObject(c8y_Connection={"status": "CONNECTED"})
    device_mgmt.device_status.assert_device_connected(
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_disconnected(
            mo=mo,
        )

    mo = ManagedObject(c8y_Connection={"status": "DISCONNECTED"})
    device_mgmt.device_status.assert_device_disconnected(
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_connected(
            mo=mo,
        )


def test_assert_availability(device_mgmt: DeviceManagement):
    """Test device availability assertions"""
    mo = ManagedObject(c8y_Availability={"status": "AVAILABLE"})
    device_mgmt.device_status.assert_device_available(
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_unavailable(
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_maintenance(
            mo=mo,
        )

    mo = ManagedObject(c8y_Availability={"status": "UNAVAILABLE"})
    device_mgmt.device_status.assert_device_unavailable(
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_available(
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_maintenance(
            mo=mo,
        )

    mo = ManagedObject(c8y_Availability={"status": "MAINTENANCE"})
    device_mgmt.device_status.assert_device_maintenance(
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_available(
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.device_status.assert_device_unavailable(
            mo=mo,
        )
