"""Retry utils"""
import re
from functools import wraps
from tenacity import (
    RetryError,
    Retrying,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)


def configure_retry(obj: object, func_name: str, **kwargs):
    """Configure retry mechanism to a function"""
    retries = kwargs.get("retries", 10)
    wait = kwargs.get("wait", 2)
    timeout = kwargs.get("timeout", 30)

    decorator = retry(
        retry=retry_if_exception_type(AssertionError),
        stop=(stop_after_delay(timeout) | stop_after_attempt(retries)),
        wait=wait_fixed(wait),
        reraise=True,
    )
    setattr(obj, func_name, decorator(getattr(obj, func_name)))


def configure_retry_on_members(obj: object, pattern: str, **kwargs):
    """Configure retry mechanism to all functions matching a pattern"""
    # apply retry mechanism
    pattern_re = re.compile(pattern)
    for name in dir(obj):
        if pattern_re.match(name, pos=0):

            def wrapper(func):
                @wraps(func)
                def retry_custom(*args, **kwargs):
                    return retrier(func, *args, **kwargs)

                return retry_custom

            setattr(obj, name, wrapper(getattr(obj, name)))


def retrier(func, *args, **kwargs):
    attempt = None
    try:
        retries = kwargs.get("retries", 10)
        wait = kwargs.get("wait", 2)
        timeout = kwargs.get("timeout", 30)

        for attempt in Retrying(
            retry=retry_if_exception_type(AssertionError),
            stop=(stop_after_delay(timeout) | stop_after_attempt(retries)),
            wait=wait_fixed(wait),
            reraise=True,
        ):
            with attempt:
                return func(*args, **kwargs)
    except RetryError as ex:
        raise ex
    except Exception as ex:
        # Append additional context information
        message = f"duration={attempt.retry_state.seconds_since_start}, attempts={attempt.retry_state.attempt_number}, timeout={timeout:.3f}s, retries={retries}, wait={wait:.3f}s"
        ex.args += (message,)
        raise ex
