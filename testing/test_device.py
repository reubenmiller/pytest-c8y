"""Device tests"""
from c8y_api.model import Device


def test_sample_device(sample_device: Device):
    """Create a sample device"""
    assert sample_device.id
