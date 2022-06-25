# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["pytest_c8y"]

package_data = {"": ["*"]}

install_requires = [
    "c8y-api>=1.3,<2.0",
    "jwt>=1.3.1,<2.0.0",
    "pytest-base-url>=2.0.0,<3.0.0",
    "pytest-html>=3.1.1,<4.0.0",
    "pytest-variables>=2.0.0,<3.0.0",
    "pytest>=7.1.2,<8.0.0",
    "python-dotenv>=0.20.0,<0.21.0",
    "requests-toolbelt>=0.9.1,<0.10.0",
    "requests>=2.26.0,<3.0.0",
    "tenacity>=8.0.1,<9.0.0",
]

entry_points = {"pytest11": ["pytest_c8y = pytest_c8y.plugin"]}

setup_kwargs = {
    "name": "pytest-c8y",
    "version": "0.0.1",
    "description": "pytest plugin for Cumulocity IoT",
    "long_description": "pytest-c8y\n===============\n\npytest-c8y is a plugin for `pytest <http://pytest.org>`_ that provides\nsupport for running `Cumulocity IoT <https://www.softwareag.cloud/site/product/cumulocity-iot.html>`_ based tests.\n\nResources\n---------\n\n- `Documentation <http://pytest-c8y.readthedocs.io/en/latest/>`_\n- `Issue Tracker <http://github.com/reubenmiller/pytest-c8y/issues>`_\n- `Code <http://github.com/reubenmiller/pytest-c8y/>`_\n",
    "author": "Reuben Miller",
    "author_email": "reuben.d.miller@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/reubenmiller/pytest-c8y",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.7.2,<4.0.0",
}


setup(**setup_kwargs)
