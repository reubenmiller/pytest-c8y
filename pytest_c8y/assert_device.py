from pytest_c8y.assert_operation import AssertOperation
from pytest_c8y.context import AssertContext
from c8y_api.model.operations import Operation
from pytest_c8y.context import AssertContext
from c8y_api.model import Operation


class AssertDevice:
    def __init__(self, context: AssertContext) -> None:
        self.context = context

    def _execute(self, **kwargs) -> AssertOperation:
        operation = Operation(
            self.context.client, self.context.device_id, **kwargs
        ).create()
        return AssertOperation(self.context, operation)
