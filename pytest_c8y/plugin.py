"""Plugin
"""
import logging
import os
import time

import pytest
from c8y_api._main_api import CumulocityApi
from c8y_api._util import c8y_keys
from c8y_api.model import Device, Operation
from dotenv import load_dotenv

from pytest_c8y.c8y import CustomCumulocityApp
from pytest_c8y.device_management import DeviceManagement, create_context_from_identity
from pytest_c8y.task import BackgroundTask
from pytest_c8y.utils import RandomNameGenerator

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", name="logger")
def logger_fixture():
    """Provide a logger for testing."""
    return logging.getLogger("c8y_api.test")


@pytest.fixture(scope="session", name="test_environment")
def test_environment_fixture(logger, variables):
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
        load_dotenv()
    defined_keys = c8y_keys()
    logger.info(f"Found the following keys: {', '.join(defined_keys)}.")


@pytest.fixture(scope="session", name="live_c8y")
def live_c8y_fixture() -> CumulocityApi:
    """Provide a live CumulocityApi instance as defined by the environment."""

    if "C8Y_BASEURL" not in os.environ:
        raise RuntimeError(
            (
                "Missing Cumulocity environment variables (C8Y_*). "
                "Cannot create CumulocityApi instance. "
                "Please define the required variables directly or setup a .env file."
            )
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
@pytest.fixture(name="sample_device")
def sample_device_fixture(logger: logging.Logger, live_c8y: CumulocityApi) -> Device:
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
def pytest_configure():
    """Configure plugin"""
    # assert config.pluginmanager.register(PyTestCumulocityPlugin(config), "pytest_c8y")


class PyTestCumulocityPlugin:
    """Ansible PyTest Plugin Class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, config):
        """Initialize plugin."""
        self.config = config


@pytest.fixture(scope="session")
def device_mgmt(live_c8y) -> DeviceManagement:
    """Provide a live CumulocityApi instance as defined by the environment."""
    return create_context_from_identity(live_c8y)


@pytest.fixture(scope="function")
def background_task(live_c8y: CumulocityApi):
    """Background task used for creating items on regular timers"""
    task = BackgroundTask(live_c8y)
    yield task
    task.stop()


@pytest.fixture(scope="function")
def background_agent(live_c8y: CumulocityApi, sample_device: Device):
    """Background agent to transition any PENDING operation to EXECUTING -> SUCCESSFUL"""
    task = BackgroundTask(live_c8y)

    def handle_operation():
        """Transition operations"""
        for operation in live_c8y.operations.select(
            agent_id=sample_device.id, status=Operation.Status.PENDING
        ):
            operation["status"] = operation.Status.EXECUTING
            time.sleep(2)
            operation["status"] = operation.Status.SUCCESSFUL

    task.start(handle_operation, interval=5)
    yield task
    task.stop()
