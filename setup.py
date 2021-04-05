#!/usr/bin/env python3

from pathlib import Path

from setuptools import find_packages, setup

packages = find_packages(exclude=("tests*",))
package_data = {pkg: ("py.typed",) for pkg in packages}

setup(
    name="zfs_timemachine",
    python_requires=">=3.8.0",
    version="0.1.10",
    description="ZFS TIME MACHINE",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/zfs_time_machine",
    packages=packages,
    package_data=package_data,
)

