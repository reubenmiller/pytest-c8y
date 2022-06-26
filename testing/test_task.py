"""Task tests"""
import time
from c8y_api.model import Device, Operation, Event
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.task import BackgroundTask


def test_background_task(
    background_task: BackgroundTask,
    sample_device: Device,
    device_mgmt: DeviceManagement,
):
    """Test running background task to create events, and run a retried assertion"""
    event = Event(
        device_mgmt.c8y,
        time="now",
        type="ci_cd",
        text="My test event",
        source=sample_device.id,
    )

    background_task.start(event.create, interval=1)

    device_mgmt.configure_retries(wait=0.25)
    device_mgmt.events.assert_count(
        source=sample_device.id, type="ci_cd", min_matches=2
    )


def test_background_agent(
    background_task: BackgroundTask,
    sample_device: Device,
    device_mgmt: DeviceManagement,
):
    """Test running background task to transition operations and run a retried assertion"""
    device_mgmt.set_device_id(sample_device.id)

    def handle_operation():
        """Transition operations"""
        for operation in device_mgmt.c8y.operations.select(
            agent_id=sample_device.id, status=Operation.Status.PENDING
        ):
            operation["status"] = operation.Status.EXECUTING
            operation.update()
            time.sleep(5)
            operation["status"] = operation.Status.SUCCESSFUL
            operation.update()

    background_task.start(handle_operation, interval=5)

    device_mgmt.create_operation(
        c8y_Restart={},
    ).assert_success()
