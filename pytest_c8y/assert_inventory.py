"""Inventory assertions
"""
import logging
from typing import Any, Dict, List
from c8y_api.model import ManagedObject
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.compare import compare_dataclass


log = logging.getLogger()


class InventoryNotFound(AssertionError):
    """Inventory not found"""


class InventoryFound(AssertionError):
    """Inventory found"""


class AssertInventory(AssertDevice):
    """Inventory assertions"""

    def assert_exists(self, inventory_id: str = None, **kwargs) -> ManagedObject:
        """Assert that an inventory managed object exists
        Args:
            inventory_id (str, optional): managed object to check if it exists. If None
                then the device_id in the context will be used.
        """
        try:
            if inventory_id is None:
                inventory_id = self.context.device_id

            return self.context.client.inventory.get(inventory_id)
        except KeyError as ex:
            raise InventoryNotFound from ex

    def assert_not_exists(self, inventory_id: str = None, **kwargs) -> None:
        """Assert that an inventory managed object does not exist

        Args:
            inventory_id (str, optional): managed object to check if it exists. If None
                then the device_id in the context will be used.
        """
        try:
            if inventory_id is None:
                inventory_id = self.context.device_id

            # expected to throw an error
            self.context.client.inventory.get(inventory_id)
            raise InventoryFound()
        except KeyError:
            return

    def assert_contains_fragment_values(
        self,
        fragments: Dict[str, Any],
        mo: ManagedObject = None,
        **kwargs,
    ) -> ManagedObject:
        """Assert the present and the values of fragments in the device managed object"""
        if mo is None:
            mo = self.context.client.inventory.get(self.context.device_id)
        assert compare_dataclass(mo.to_json(), fragments)
        return mo

    def assert_contains_fragments(
        self,
        fragments: List[str],
        mo: ManagedObject = None,
        **kwargs,
    ) -> ManagedObject:
        """Assert the present of fragments in the device managed object (regardless of value)"""
        if mo is None:
            mo = self.context.client.inventory.get(self.context.device_id)

        mo_dict = mo.to_json()
        missing = [key for key in fragments if key not in mo_dict]
        assert (
            missing == []
        ), f"Device is missing some fragments. wanted={missing}, got={list(mo_dict.keys())}"
        return mo

    def assert_changed(
        self,
        reference_object: Dict[str, Any],
        fragment: str,
        mo: ManagedObject = None,
        **kwargs,
    ) -> ManagedObject:
        """Assert that the device managed object has changed from the given reference object.
        The comparison is limited to a fragment if it is provided.
        """
        reference = reference_object.get(fragment) if fragment else reference_object

        if mo is None:
            mo = self.context.client.inventory.get(self.context.device_id)
        assert not compare_dataclass(mo.to_json().get(fragment), reference)

    def assert_child_device_count(
        self, min_count: int = 1, max_count: int = None, **kwargs
    ) -> List[Dict[str, Any]]:
        """Assert that a device has a specific number of child devices"""
        response = self.context.client.get(
            f"/inventory/managedObjects/{self.context.device_id}/childDevices",
            params={
                "pageSize": 2000,
            },
        )

        children = response.get("references")

        if min_count is not None:
            assert (
                len(children) >= min_count
            ), f"Expected total child devices count to be greater than or equal to {min_count}"

        if max_count is not None:
            assert (
                len(children) <= max_count
            ), f"Expected total child devices count to be less than or equal to {max_count}"

        return children

    def assert_child_device_names(
        self, *expected_devices: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """Assert that a device has child devices with the specified names"""
        response = self.context.client.get(
            f"/inventory/managedObjects/{self.context.device_id}/childDevices"
        )

        children = []
        for child in response.get("references"):
            child_mo = child.get("managedObject", {})
            if child_mo:
                children.append(child_mo)

        assert sorted(expected_devices) == sorted(map(lambda x: x["name"], children))
        return children

    def assert_relationship(
        self,
        child_identity: str,
        child_identity_type: str = "c8y_Serial",
        child_type: str = "childDevices",
        mo: ManagedObject = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """Assert that a child identity is a child of a give managed object

        Args:
            child_identity (str): Child identity name
            child_identity_type (str, optional): Child identity type. Defaults to 'c8y_Serial'
            child_type (str, optional): Child relationship type, e.g. childDevices, childAssets, childAdditions.
                Defaults to 'childDevices'
            mo (ManagedObject, optional): Managed Object (parent) object. If set to None, then the
                current context is used.
        """

        child_id = ""
        try:
            child_identity_obj = self.context.client.identity.get(
                child_identity, child_identity_type
            )
            child_id = child_identity_obj.managed_object_id
            assert child_id, "Child id should not be empty"
        except KeyError as ex:
            raise InventoryNotFound from ex

        try:
            mo_id = self.context.device_id
            if mo is not None:
                mo_id = mo.id
            return self.context.client.get(
                f"/inventory/managedObjects/{mo_id}/childDevices/{child_id}"
            )
        except KeyError as ex:
            raise InventoryNotFound from ex

    def delete_device_and_user(
        self,
        mo: ManagedObject = None,
        **kwargs,
    ) -> None:
        """Assert device user and all child devices. The device user is then deleted afterwards"""

        try:
            if mo is None:
                mo = self.context.client.inventory.get(self.context.device_id)

            log.info(
                "Removing managed object and all child devices. id=%s",
                mo.id,
            )

            self.context.client.delete(
                f"/inventory/managedObjects/{mo.id}",
                params={
                    "cascade": True,
                    "withDeviceUser": False,
                },
            )

            log.info("Removing device user. name=%s", mo.owner)
            tenant_id = self.context.client.tenant_id
            self.context.client.delete(f"/user/{tenant_id}/users/{mo.owner}")
        except KeyError as ex:
            log.info("Device has already been removed. %s", ex)
        except Exception as ex:
            log.error("Could not delete device. %s", ex)
            raise
