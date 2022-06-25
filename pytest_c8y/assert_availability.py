from c8y_api.model import ManagedObject
from pytest_c8y.assert_device import AssertDevice


class AssertDeviceAvailability(AssertDevice):
    class ConnectionStatus:
        CONNECTED = "CONNECTED"
        DISCONNECTED = "DISCONNECTED"

    class AvailabilityStatus:
        AVAILABLE = "AVAILABLE"
        UNAVAILABLE = "UNAVAILABLE"
        MAINTENANCE = "MAINTENANCE"

    def assert_device_available(self, **kwargs) -> ManagedObject:
        """Assert that the device availability status (c8y_Availability.status) is set to AVAILABLE"""
        mo = self.context.client.inventory.get(self.context.device_id)
        return mo["c8y_Availability"]["status"] == self.AvailabilityStatus.AVAILABLE

    def assert_device_unavailable(self, **kwargs) -> ManagedObject:
        """Assert that the device availability status (c8y_Availability.status) is set to UNAVAILABLE"""
        mo = self.context.client.inventory.get(self.context.device_id)
        return mo["c8y_Availability"]["status"] == self.AvailabilityStatus.UNAVAILABLE

    def assert_device_maintenance(self, **kwargs) -> ManagedObject:
        """Assert that the device availability status (c8y_Availability.status) is set to MAINTENANCE"""
        mo = self.context.client.inventory.get(self.context.device_id)
        return mo["c8y_Availability"]["status"] == self.AvailabilityStatus.MAINTENANCE

    def assert_device_connected(self, **kwargs) -> ManagedObject:
        """Assert that the device connection status (c8y_Availability.status) is set to CONNECTED"""
        mo = self.context.client.inventory.get(self.context.device_id)
        return mo["c8y_Connection"]["status"] == self.ConnectionStatus.CONNECTED

    def assert_device_disconnected(self, **kwargs) -> ManagedObject:
        """Assert that the device connection status (c8y_Connection.status) is set to DISCONNECTED"""
        mo = self.context.client.inventory.get(self.context.device_id)
        return mo["c8y_Connection"]["status"] == self.ConnectionStatus.CONNECTED

    def create_operation(self, **kwargs):
        fragments = {
            "description": "Send operation",
            **kwargs,
        }
        return self._execute(**fragments)
