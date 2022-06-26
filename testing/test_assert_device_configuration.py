"""Assert device configuration tests"""
from c8y_api.model import Device
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.utils import RandomNameGenerator
from pytest_c8y.models import Configuration


def test_set_configuration(sample_device: Device, device_mgmt: DeviceManagement):
    """Test set configuration"""
    device_mgmt.set_device_id(sample_device.id)
    name = RandomNameGenerator.random_name() + ".txt"
    contents = "Some text"

    with device_mgmt.binaries.new_binary(
        name, binary_type="ci_cd", contents=contents
    ) as binary:
        url = (
            device_mgmt.context.client.base_url
            + device_mgmt.context.client.binaries.build_object_path(binary.id)
        )
        operation = device_mgmt.configuration.set_configuration(
            Configuration(type="CUSTOM", url=url)
        )
        operation.assert_pending()

        assert operation.operation.to_json()["c8y_DownloadConfigFile"]["url"] == url
        assert (
            operation.operation.to_json()["c8y_DownloadConfigFile"]["type"] == "CUSTOM"
        )


def test_get_configuration(sample_device: Device, device_mgmt: DeviceManagement):
    """Test get configuration"""
    device_mgmt.set_device_id(sample_device.id)
    name = RandomNameGenerator.random_name() + ".txt"
    contents = "Some text"

    operation = device_mgmt.configuration.get_configuration(
        Configuration(type="CUSTOM")
    )
    operation.assert_pending()
    assert operation.operation.to_json()["c8y_UploadConfigFile"]["type"] == "CUSTOM"
