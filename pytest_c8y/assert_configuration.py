"""Device configuration assertions"""
from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.models import Configuration
from pytest_c8y.assert_operation import AssertOperation


class DeviceConfiguration(AssertDevice):
    """Device configuration assertions"""

    def set_configuration(
        self, configuration: Configuration, **kwargs
    ) -> AssertOperation:
        """Create a configuration operation c8y_DownloadConfigFile
        This should trigger the device/agent to download the configuration from the provided url
        """
        config_type = configuration.__dict__.get("type", "")
        fragments = {
            "description": f"Send configuration snapshot {config_type} to device",
            "c8y_DownloadConfigFile": configuration.__dict__,
            **kwargs,
        }
        return self._execute(**fragments)

    def get_configuration(
        self, configuration: Configuration, **kwargs
    ) -> AssertOperation:
        """Create a configuration operation (c8y_UploadConfigFile) to get the configuration
        from a device.

        This should trigger the device/agent to uploaded the configuration type to the platform
        """
        config_type = configuration.__dict__.get("type", "")
        fragments = {
            "description": f"Retrieve {config_type} configuration snapshot from device",
            "c8y_UploadConfigFile": configuration.__dict__,
            **kwargs,
        }
        return self._execute(**fragments)
