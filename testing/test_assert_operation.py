"""Assert operation tests"""
from c8y_api.model import Device, Operation
from c8y_test_core.device_management import DeviceManagement


def test_assert_operation_status(sample_device: Device, device_mgmt: DeviceManagement):
    """Test operation status assertion"""
    device_mgmt.set_device_id(sample_device.id)
    operation = device_mgmt.create_operation(c8y_Restart={})

    operation.assert_pending()

    operation.operation["status"] = Operation.Status.EXECUTING
    operation.operation.update()
    operation.assert_not_pending()

    operation.operation["status"] = Operation.Status.SUCCESSFUL
    operation.operation.update()
    operation.assert_success(timeout=1)

    operation.operation["status"] = Operation.Status.FAILED
    operation.operation["failureReason"] = "Something went wrong"
    operation.operation.update()
    operation.assert_failed("^Something.+")
