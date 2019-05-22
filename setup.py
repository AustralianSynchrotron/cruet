"""
cruet
---------
cruet is a toolkit for creating microservices with flask.
"""
import io
import re
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with io.open("cruet/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setup(
    name="cruet",
    version=version,
    license="BSD",
    author="Scientific Computing - Australian Synchrotron",
    author_email="ascomputing@ansto.gov.au",
    description="A toolkit for building microservices with flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AustralianSynchrotron/cruet",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
