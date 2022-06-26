"""Command assertion tests"""
from c8y_api.model import Device
from pytest_c8y.device_management import DeviceManagement


def test_execute_command(sample_device: Device, device_mgmt: DeviceManagement):
    """Test execute command"""
    device_mgmt.set_device_id(sample_device.id)

    operation = device_mgmt.command.execute("ls -l")
    assert operation.operation.to_json()["c8y_Command"]["text"] == "ls -l"
    operation.assert_pending()
