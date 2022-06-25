"""Command assertions"""
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.assert_operation import AssertOperation


class Command(AssertDevice):
    def execute(self, text: str, **kwargs) -> AssertOperation:
        """Execute a shell command via an operation"""
        fragments = {
            "description": "Execute shell command",
            "c8y_Command": {
                "text": text,
            },
            **kwargs,
        }
        return self._execute(**fragments)
