"""Software management"""
import dataclasses
import re

from c8y_api.model import ManagedObject

from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.assert_operation import AssertOperation
from pytest_c8y.models import Software


class SoftwareManagement(AssertDevice):
    """Software management"""

    class Action:
        """Software actions."""

        # pylint: disable=too-few-public-methods

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
            "description": "Install software: "
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
            "description": "Install software: "
            + ",".join(software.name for software in software_list),
            "c8y_SoftwareList": [
                {**software.__dict__, "action": self.Action.INSTALL}
                for software in software_list
            ],
            **kwargs,
        }
        return self._execute(**fragments)

    class Reasons:
        # pylint: disable=too-few-public-methods

        """Error reasons"""
        MISSING = "MISSING"
        INSTALLED = "INSTALLED"
        VERSION_MISMATCH = "VERSION_MISMATCH"
        VERSION_MATCH = "VERSION_MATCH"

    def assert_software_installed(
        self, *expected_software_list: Software, mo: ManagedObject = None
    ):
        """Assert that a list of software packages are installed.
        If the version is empty, then version matching is skipped.
        """
        if mo is None:
            mo = self.context.client.inventory.get(self.context.device_id)

        installed = [item["name"] for item in mo["c8y_SoftwareList"]]
        errors = []

        for exp_software in expected_software_list:
            if exp_software.name not in installed:
                errors.append((exp_software.name, self.Reasons.MISSING))
                continue

            if not exp_software.version:
                continue

            # version check
            version_pattern = re.compile(exp_software.version)
            for current_software in mo["c8y_SoftwareList"]:
                if current_software[
                    "name"
                ] == exp_software.name and version_pattern.match(
                    current_software["version"]
                ):
                    break
            else:
                errors.append((exp_software.name, self.Reasons.VERSION_MISMATCH))

        assert len(errors) == 0, (
            "Software not installed. "
            f"errors={errors}, wanted={expected_software_list}, got={mo['c8y_SoftwareList']}"
        )

    def assert_not_software_installed(
        self, *unexpected_software_list: Software, mo: ManagedObject = None
    ):
        """Assert that a list of software packages are not installed.
        If the version is empty, then version matching is skipped.
        """
        if mo is None:
            mo = self.context.client.inventory.get(self.context.device_id)

        installed = [item["name"] for item in mo["c8y_SoftwareList"]]
        errors = []

        for exp_software in unexpected_software_list:
            if exp_software.name in installed and not exp_software.version:
                errors.append((exp_software.name, self.Reasons.INSTALLED))
                continue

            # version check
            version_pattern = re.compile(exp_software.version)
            for current_software in mo["c8y_SoftwareList"]:
                if current_software[
                    "name"
                ] == exp_software.name and version_pattern.match(
                    current_software["version"]
                ):
                    errors.append((exp_software.name, self.Reasons.VERSION_MATCH))
                    break

        assert len(errors) == 0, (
            "Unwanted software installed. "
            f"errors={errors}, unwanted={unexpected_software_list}, got={mo['c8y_SoftwareList']}"
        )
