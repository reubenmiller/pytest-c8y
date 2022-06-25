from typing import List
from pytest_c8y.assert_device import AssertDevice
from c8y_api.model import ManagedObject

from pytest_c8y.models import Firmware


class AssertMeasurements(AssertDevice):
    def _get_supported_series(self) -> List[str]:
        response = self.context.client.get(
            f"inventory/managedObjects/{self.context.device_id}/supportedSeries"
        )
        return response["c8y_SupportedSeries"]

    def assert_supported_series(
        self, expected_series: List[str], **kwargs
    ) -> ManagedObject:
        missing = []
        current_series = self._get_supported_series()
        for name in expected_series:
            if name not in current_series:
                missing.append(name)

        assert (
            len(missing) == 0
        ), f"Device is missing some series. wanted={expected_series}, got={current_series}"

    def assert_supported_contains(
        self, expected_series: List[str], **kwargs
    ) -> ManagedObject:
        assert sorted(self._get_supported_series()) == sorted(expected_series), ""

    def assert_not_firmware(self, expected_firmware: Firmware):
        mo = self.context.client.inventory.get(self.context.device_id)
        assert mo["c8y_Firmware"] != expected_firmware
        return mo

    def assert_measurement_count(
        self, exp_min_count: int = 1, exp_max_count: int = None, **kwargs
    ):
        raise NotImplementedError(
            "TODO: c8y_api does not support count api or statistics fragment"
        )
