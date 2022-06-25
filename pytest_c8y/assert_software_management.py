import dataclasses
from typing import List
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.assert_operation import AssertOperation

from pytest_c8y.models import Software


class SoftwareManagement(AssertDevice):
    class Action:
        """Software actions."""

        INSTALL = "install"
        DELETE = "delete"

    def install(self, *software_list: Software, **kwargs) -> AssertOperation:
        """Install software on a device via the c8y_SoftwareUpdate operation."""
        items = []
        for software in software_list:
            items.append(dataclasses.replace(software, action=self.Action.INSTALL))
        return self.update(*items, **kwargs)

    def update(self, *software_list: Software, **kwargs) -> AssertOperation:
        """Install or delete software on a device via the c8y_SoftwareUpdate operation.
        The software can be marked as install or delete
        """
        fragments = {
            "description": f"Install software: "
            + ",".join(software.name for software in software_list),
            "c8y_SoftwareUpdate": [software.__dict__ for software in software_list],
            **kwargs,
        }
        return self._execute(**fragments)

    def remove(self, *software_list: Software, **kwargs) -> AssertOperation:
        """Remove software on a device via the c8y_SoftwareUpdate operation."""
        items = []
        for software in software_list:
            items.append(dataclasses.replace(software, action=self.Action.DELETE))
        return self.update(*items, **kwargs)

    def replace(self, *software_list: Software, **kwargs) -> AssertOperation:
        """Replace the software list on a device via the c8y_SoftwareList operation"""
        fragments = {
            "description": f"Install software: "
            + ",".join(software.name for software in software_list),
            "c8y_SoftwareList": [
                {**software.__dict__, "action": self.Action.INSTALL}
                for software in software_list
            ],
            **kwargs,
        }
        return self._execute(**fragments)

    def assert_software_installed(self, expected_software_list: List[Software]):
        mo = self.context.client.inventory.get(self.context.device_id)

        missing = []
        version_mismatch = []
        installed = [item["name"] for item in mo["c8y_SoftwareList"]]

        for item in expected_software_list:
            if item.name not in installed:
                missing.append(item.name)
            else:
                version_mismatch

    def assert_not_software_installed(self, software_list: List[str]):
        mo = self.context.client.inventory.get(self.context.device_id)

        installed_but_is = []
        for item in mo["c8y_SoftwareList"]:
            if item.name in software_list:
                installed_but_is.append(item.name)

        assert installed_but_is == []
