import re
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)


def configure_retry(obj, func_name, **kwargs):
    retries = kwargs.get("retries", 10)
    wait = kwargs.get("wait", 2)
    timeout = kwargs.get("timeout", 5)

    decorator = retry(
        retry=retry_if_exception_type(AssertionError),
        stop=(stop_after_delay(timeout) | stop_after_attempt(retries)),
        wait=wait_fixed(wait),
        reraise=True,
    )
    setattr(obj, func_name, decorator(getattr(obj, func_name)))


def configure_retry_on_members(obj: object, pattern: str):
    # apply retry mechanism
    pattern_re = re.compile(pattern)
    for name in dir(obj):
        if pattern_re.match(name, pos=0):
            configure_retry(obj, name)
