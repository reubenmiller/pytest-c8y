from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.assert_operation import AssertOperation
from c8y_api.model import ManagedObject

from pytest_c8y.models import Firmware


class FirmwareManagement(AssertDevice):
    def install(self, firmware: Firmware, **kwargs) -> AssertOperation:
        """Install firmware via the c8y_Firmware operation"""
        fragments = {
            "description": f"Install firmware: {firmware.name}={firmware.version}",
            "c8y_Firmware": firmware.__dict__,
            **kwargs,
        }
        return self._execute(**fragments)

    def assert_firmware(self, expected_firmware: Firmware) -> ManagedObject:
        mo = self.context.client.inventory.get(self.context.device_id)
        assert mo["c8y_Firmware"] == expected_firmware
        return mo

    def assert_not_firmware(self, expected_firmware: Firmware):
        mo = self.context.client.inventory.get(self.context.device_id)
        assert mo["c8y_Firmware"] != expected_firmware
        return mo
