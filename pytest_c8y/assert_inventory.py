"""Inventory assertions
"""
from typing import Any, Dict, List
from c8y_api.model import ManagedObject
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.compare import compare_dataclass


class AssertInventory(AssertDevice):
    """Inventory assertions"""

    def assert_contains_fragment_values(
        self, fragments: Dict[str, Any], **kwargs
    ) -> ManagedObject:
        """Assert the present and the values of fragments in the device managed object"""
        mo = self.context.client.inventory.get(self.context.device_id)
        assert compare_dataclass(mo, fragments)
        return mo

    def assert_contains_fragments(
        self, fragments: List[str], **kwargs
    ) -> ManagedObject:
        """Assert the present of fragments in the device managed object (regardless of value)"""
        mo = self.context.client.inventory.get(self.context.device_id)

        missing = [key for key in fragments if key not in mo]
        assert (
            missing == []
        ), f"Device is missing some fragments. wanted={missing}, got={mo.keys()}"
        return mo

    def assert_changed(
        self, reference_object: Dict[str, Any], fragment: str
    ) -> ManagedObject:
        """Assert that the device managed object has changed from the given reference object.
        The comparison is limited to a fragment if it is provided.
        """
        reference = reference_object.get(fragment) if fragment else reference_object

        mo = self.context.client.inventory.get(self.context.device_id)
        assert not compare_dataclass(mo.get(fragment), reference)

    def assert_child_device_names(
        self, expected_devices: List[str]
    ) -> List[Dict[str, Any]]:
        response = self.context.client.get(
            f"inventory/managedObjects/{self.context.device_id}/childDevices"
        )

        children = []
        for child in response.get("references"):
            children += {
                "id": child.get("id"),
                "name": child.get("name"),
            }

        assert sorted(expected_devices) == sorted(map(lambda x: x["name"], children))
        return children
