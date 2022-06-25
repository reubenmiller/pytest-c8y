import requests
from pytest_c8y.assert_device import AssertDevice
from c8y_api.model import ManagedObject


class DeviceNotFound(AssertionError):
    """Device not found"""


class AssertIdentity(AssertDevice):
    def assert_exists(
        self, external_id: str, external_type: str = "c8y_Serial", **kwargs
    ) -> ManagedObject:
        try:
            mo = self.context.client.identity.get_object(
                external_id=external_id, external_type=external_type
            )
        except requests.HTTPError as ex:
            if ex.response.status_code == 404:
                raise DeviceNotFound()
            raise

        assert mo
        return mo
