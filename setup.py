from setuptools import setup, find_packages
import os

__name="pycncnettunnel"

setup(
    name=__name,
    version="0.1.0",
    description="Test tunnel for CNCNet's YR",
    url="https://github.com/shmocz/pycncnettunnel",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: 3.8",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["{n}={n}.main:main".format(n=__name)]},
)
