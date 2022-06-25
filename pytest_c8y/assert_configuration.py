from pytest_c8y.assert_device import AssertDevice
from pytest_c8y.models import Configuration


class DeviceConfiguration(AssertDevice):
    def set_configuration(self, configuration: Configuration, **kwargs):
        """Create a configuration operation c8y_DownloadConfigFile
        This should trigger the device/agent to download the configuration from the provided url
        """
        fragments = {
            "c8y_DownloadConfigFile": configuration.__dict__,
            **kwargs,
        }
        return self._execute(**fragments)

    def get_configuration(self, configuration: Configuration, **kwargs):
        """Create a configuration operation (c8y_UploadConfigFile) to get the configuration from a device.
        This should trigger the device/agent to uploaded the configuration type to the platform
        """
        fragments = {
            "c8y_UploadConfigFile": configuration.__dict__,
            **kwargs,
        }
        return self._execute(**fragments)
