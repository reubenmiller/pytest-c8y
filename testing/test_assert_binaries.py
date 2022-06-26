"""Assert binaries tests"""
from pytest_c8y.device_management import DeviceManagement
from pytest_c8y.utils import RandomNameGenerator


def test_binary_context(device_mgmt: DeviceManagement):
    """Test binary context"""
    name = RandomNameGenerator.random_name() + ".txt"
    contents = "Some text"

    with device_mgmt.binaries.new_binary(
        name, binary_type="ci_cd", contents=contents
    ) as binary:
        assert binary.id
        url = (
            device_mgmt.context.client.base_url
            + device_mgmt.context.client.binaries.build_object_path(binary.id)
        )
        assert url
        # assert binary["url"]
