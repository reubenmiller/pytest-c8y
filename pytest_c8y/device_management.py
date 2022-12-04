"""Device management assertions
"""
import logging

from c8y_api import CumulocityApi

from pytest_c8y.assert_availability import AssertDeviceAvailability
from pytest_c8y.assert_binaries import Binaries
from pytest_c8y.assert_command import Command
from pytest_c8y.assert_configuration import DeviceConfiguration
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.assert_alarms import Alarms
from pytest_c8y.assert_events import Events
from pytest_c8y.assert_firmware import FirmwareManagement
from pytest_c8y.assert_identity import AssertIdentity
from pytest_c8y.assert_logfile import DeviceLogFile
from pytest_c8y.assert_inventory import AssertInventory
from pytest_c8y.assert_measurements import AssertMeasurements
from pytest_c8y.assert_operation import AssertOperation
from pytest_c8y.assert_software_management import SoftwareManagement
from pytest_c8y.context import AssertContext
from pytest_c8y.retry import configure_retry_on_members


class DeviceManagement(AssertDevice):
    """Device management assertions"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, context: AssertContext) -> None:
        super().__init__(context)

        self.binaries = Binaries(context)
        self.command = Command(context)
        self.configuration = DeviceConfiguration(context)
        self.logs = DeviceLogFile(context)
        self.device_status = AssertDeviceAvailability(context)
        self.alarms = Alarms(context)
        self.events = Events(context)
        self.firmware_management = FirmwareManagement(context)
        self.identity = AssertIdentity(context)
        self.inventory = AssertInventory(context)
        self.measurements = AssertMeasurements(context)
        self.software_management = SoftwareManagement(context)

    @property
    def c8y(self) -> CumulocityApi:
        """Shortcut to context.client"""
        return self.context.client

    def configure_retries(self, **kwargs):
        """Configure retries for all assertions"""
        # apply retry mechanism
        for member in dir(self):
            current_property = getattr(self, member)
            if isinstance(current_property, AssertDevice):
                configure_retry_on_members(current_property, "^assert_.+", **kwargs)

    def set_device_id(self, device_id: str) -> "DeviceManagement":
        """Set the current device id to be used in all assertions"""
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

    def create_operation(self, **kwargs) -> AssertOperation:
        """Create an operation"""
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
    """Create a context from a device identity"""
    context = AssertContext(client=c8y, device_id=device_id, log=logging.getLogger())
    if not device_id and external_id:
        context.device_id = c8y.identity.get_id(external_id, external_type)
    return DeviceManagement(context)
