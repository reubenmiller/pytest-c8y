"""Measurement assertions"""
from typing import List

from c8y_api.model import ManagedObject

from pytest_c8y.assert_device import AssertDevice


class AssertMeasurements(AssertDevice):
    """Measurement assertions"""

    def _get_supported_series(self) -> List[str]:
        response = self.context.client.get(
            f"inventory/managedObjects/{self.context.device_id}/supportedSeries"
        )
        return response["c8y_SupportedSeries"]

    def assert_supported_series_contains(self, *expected_series: str) -> ManagedObject:
        """Assert presence of a subset of series in the supported series list"""
        missing = []
        current_series = self._get_supported_series()
        for name in expected_series:
            if name not in current_series:
                missing.append(name)

        assert (
            len(missing) == 0
        ), f"Device is missing some series. wanted={expected_series}, got={current_series}"

    def assert_supported_series(
        self,
        *expected_series: str,
    ) -> ManagedObject:
        """Assert exact supported series"""

        wanted = sorted(expected_series)
        got = sorted(self._get_supported_series())
        assert got == wanted, f"wanted={wanted}, got={got}"

    def assert_count(
        self,
        _exp_min_count: int = 1,
        _exp_max_count: int = None,
    ):
        """Assert a minimum measurement count"""
        raise NotImplementedError(
            "TODO: c8y_api does not support count api or statistics fragment."
        )
