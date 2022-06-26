"""Software management tests"""
from c8y_api.model import ManagedObject
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.models import Software
import pytest


def test_software_management_install(device_mgmt: DeviceManagement):
    """Test software installed assertion"""
    mo = ManagedObject(
        c8y_SoftwareList=[
            Software(name="test01", version="1.0.0").__dict__,
            Software(name="test02", version="1.2.0").__dict__,
        ]
    )
    device_mgmt.software_management.assert_software_installed(
        Software(name="test01", version="1.0.0"),
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.software_management.assert_not_software_installed(
            Software(name="test01", version="1.0.0"),
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.software_management.assert_software_installed(
            Software(name="not-exists"),
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.software_management.assert_software_installed(
            Software(name="test01", version="1.1.0"),
            mo=mo,
        )


def test_software_management_not_install(device_mgmt: DeviceManagement):
    """Test software not installed assertion"""
    mo = ManagedObject(
        c8y_SoftwareList=[
            Software(name="test01", version="1.0.0").__dict__,
            Software(name="test02", version="1.2.0").__dict__,
        ]
    )
    device_mgmt.software_management.assert_not_software_installed(
        Software(name="test03"),
        mo=mo,
    )

    with pytest.raises(AssertionError):
        device_mgmt.software_management.assert_not_software_installed(
            Software(name="test02"),
            mo=mo,
        )

    with pytest.raises(AssertionError):
        device_mgmt.software_management.assert_not_software_installed(
            Software(name="test01", version="1.0.0"),
            mo=mo,
        )
