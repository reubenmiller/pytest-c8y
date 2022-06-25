import logging
from pytest_c8y.assert_configuration import DeviceConfiguration

from pytest_c8y.context import AssertContext
from pytest_c8y.assert_software_management import SoftwareManagement
from pytest_c8y.assert_firmware import FirmwareManagement
from pytest_c8y.assert_operation import AssertOperation
from pytest_c8y.assert_inventory import AssertInventory
from pytest_c8y.assert_measurements import AssertMeasurements
from pytest_c8y.assert_availability import AssertDeviceAvailability
from pytest_c8y.assert_command import Command
from pytest_c8y.assert_events import Events
from pytest_c8y.assert_binaries import Binaries
from pytest_c8y.assert_identity import AssertIdentity

from c8y_api import CumulocityApi
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.retry import configure_retry, configure_retry_on_members


class DeviceManagement(AssertDevice):
    def __init__(self, context: AssertContext) -> None:
        super().__init__(context)

        self.binaries = Binaries(context)
        self.command = Command(context)
        self.configuration = DeviceConfiguration(context)
        self.device_status = AssertDeviceAvailability(context)
        self.events = Events(context)
        self.firmware_management = FirmwareManagement(context)
        self.identity = AssertIdentity(context)
        self.inventory = AssertInventory(context)
        self.measurements = AssertMeasurements(context)
        self.software_management = SoftwareManagement(context)

        self._configure_retries()

    def _configure_retries(self):
        # apply retry mechanism
        for member in dir(self):
            current_property = getattr(self, member)
            if isinstance(current_property, AssertDevice):
                configure_retry_on_members(current_property, "^assert_.+")

    def set_device_id(self, device_id: str) -> "DeviceManagement":
        self.context.device_id = device_id
        return self

    def restart(self, **kwargs) -> AssertOperation:
        """Send a restart operation to the device"""
        fragments = {
            "description": "Restart device",
            "c8y_Restart": {},
            **kwargs,
        }
        return self._execute(**fragments)

    def create_operation(self, **kwargs):
        fragments = {
            "description": "Send operation",
            **kwargs,
        }
        return self._execute(**fragments)


def create_context_from_identity(
    c8y: CumulocityApi,
    device_id: str = None,
    external_id: str = None,
    external_type: str = None,
) -> "DeviceManagement":
    context = AssertContext(client=c8y, device_id=device_id, log=logging.getLogger())
    if not device_id and external_id:
        context.device_id = c8y.identity.get_id(external_id, external_type)
    return DeviceManagement(context)
