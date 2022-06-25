import re
from typing import List
from pytest_c8y.assert_device import AssertDevice
from c8y_api.model import Event


class Events(AssertDevice):
    def assert_count(
        self, expected_text: str, min_matches: int = 1, **kwargs
    ) -> List[Event]:
        """Assert a minimum count of matches events."""
        events = self.context.client.events.get_all(
            source=self.context.device_id, page_size=10, **kwargs
        )
        text_pattern = re.compile(expected_text, re.IGNORECASE)
        matching_events = filter(text_pattern.match, events)

        assert (
            len(matching_events) < min_matches
        ), f"Event count is less than expected. wanted={min_matches} (min), got={len(matching_events)}"
        return matching_events
