import logging
import os

import pytest

from pytest_c8y.device_management import DeviceManagement, create_context_from_identity
from pytest_c8y.c8y import CustomCumulocityApp

LOGGER = logging.getLogger(__name__)

# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

# pylint: disable=redefined-outer-name

import logging
import os

# TODO: dotenv is broken on macos arm64
# from dotenv import load_dotenv
import pytest

from c8y_api._main_api import CumulocityApi
from c8y_api._util import c8y_keys
from c8y_api.model import Device

from .utils import RandomNameGenerator


def load_dotenv(filename=".env"):
    if os.path.exists(filename):
        with open(filename) as file:
            for line in file:
                key, _, value = line.partition("=")
                os.environ[key] = value


@pytest.fixture(scope="session")
def safe_executor(logger):
    """A safe function execution wrapper.
    This provides a `execute(fun)` function which catches/logs all
    exceptions. It returns True if the wrapped function was executed
    without error, False otherwise.
    """
    # pylint: disable=broad-except

    def execute(fun) -> bool:
        try:
            fun()
            return True
        except BaseException as e:
            logger.warning(f"Caught exception ignored due to safe call: {e}")
        return False

    return execute


@pytest.fixture(scope="session")
def logger():
    """Provide a logger for testing."""
    return logging.getLogger("c8y_api.test")


@pytest.fixture(scope="session")
def test_environment(logger, variables):
    """Prepare the environment, i.e. read a .env file if found."""

    logger.warning(f"Found variables: {variables}")

    # check if there is a .env file
    if os.path.exists(".env"):
        logger.info("Environment file (.env) exists and will be considered.")
        # check if any C8Y_ variable is already defined
        predefined_keys = c8y_keys()
        if predefined_keys:
            logger.fatal(
                "The following environment variables are already defined and may be overridden: "
                + ", ".join(predefined_keys)
            )
        # TODO: dotenv is broken on macos arm64

        # load_dotenv()
    # list C8Y_* keys
    defined_keys = c8y_keys()
    logger.info(f"Found the following keys: {', '.join(defined_keys)}.")


@pytest.fixture(scope="session")
def live_c8y(test_environment) -> CumulocityApi:
    """Provide a live CumulocityApi instance as defined by the environment."""

    if "C8Y_BASEURL" not in os.environ.keys():
        raise RuntimeError(
            "Missing Cumulocity environment variables (C8Y_*). Cannot create CumulocityApi instance. "
            "Please define the required variables directly or setup a .env file."
        )
    return CustomCumulocityApp()


@pytest.fixture(scope="session")
def factory(logger, live_c8y: CumulocityApi):
    """Provides a generic object factory function which ensures that created
    objects are removed after testing."""

    created = []

    def factory_fun(obj):
        if not obj.c8y:
            obj.c8y = live_c8y
        o = obj.create()
        logger.info(f"Created object #{o.id}, ({o.__class__.__name__})")
        created.append(o)
        return o

    yield factory_fun

    for c in created:
        c.delete()
        logger.info(f"Removed object #{c.id}, ({c.__class__.__name__})")


# @pytest.fixture(scope='session')
@pytest.fixture()
def sample_device(logger: logging.Logger, live_c8y: CumulocityApi) -> Device:
    """Provide an sample device, just for testing purposes."""

    typename = RandomNameGenerator.random_name()
    device = Device(
        live_c8y, type=typename, name=typename, com_cumulocity_model_Agent={}
    ).create()
    logger.info(f"Created test device #{device.id}, name={device.name}")

    yield device

    device.delete()
    logger.info(f"Deleted test device #{device.id}")


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Configure plugin"""
    # assert config.pluginmanager.register(PyTestCumulocityPlugin(config), "pytest_c8y")


class PyTestCumulocityPlugin:
    """Ansible PyTest Plugin Class."""

    def __init__(self, config):
        """Initialize plugin."""
        self.config = config


@pytest.fixture(scope="session")
def device_mgmt(live_c8y) -> DeviceManagement:
    """Provide a live CumulocityApi instance as defined by the environment."""
    return create_context_from_identity(live_c8y)
