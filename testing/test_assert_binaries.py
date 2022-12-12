"""Assert binaries tests"""
from c8y_test_core.device_management import DeviceManagement
from c8y_test_core.utils import RandomNameGenerator


def test_binary_context(device_mgmt: DeviceManagement):
    """Test binary context"""
    name = RandomNameGenerator.random_name() + ".txt"
    contents = "Some text"

    with device_mgmt.binaries.new_binary(
        name, binary_type="ci_cd", contents=contents
    ) as ref:
        assert ref.binary.id
        assert ref.url
