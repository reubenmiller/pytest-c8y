"""Event assertions"""
import re
from typing import List

from c8y_api.model import Event

from pytest_c8y.assert_device import AssertDevice


class EventNotFound(AssertionError):
    """Event not found"""


class Events(AssertDevice):
    """Event assertions"""

    # pylint: disable=too-few-public-methods

    def assert_count(
        self, expected_text: str = None, min_matches: int = 1, **kwargs
    ) -> List[Event]:
        """Assert a minimum count of matches events."""
        source = kwargs.pop("source", self.context.device_id)
        events = self.context.client.events.get_all(source=source, **kwargs)

        matching_events = events
        if expected_text:
            text_pattern = re.compile(expected_text, re.IGNORECASE)
            matching_events = list(filter(lambda x: text_pattern.match(x.text), events))

        assert len(matching_events) >= min_matches, (
            "Event count is less than expected. "
            f"wanted={min_matches} (min), got={len(matching_events)}"
        )
        return matching_events

    def assert_exists(self, event_id: str) -> Event:
        """Assert that an event exists and return it if found"""
        try:
            return self.context.client.events.get(event_id)
        except KeyError as ex:
            raise EventNotFound() from ex
