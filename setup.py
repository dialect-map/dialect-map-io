# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


# Package meta-data
NAME = "dialect-map-io"
INFO = "Python package containing the I/O functionality for the Dialect Map jobs"
URL = "https://github.com/dialect-map/dialect-map-io"
REQUIRES_PYTHON = ">=3.7, <4"
AUTHORS = "NYU DS3 Team"
VERSION = open("VERSION", "r").read().strip()


# Package requirements
INSTALLATION_REQS = [
    "pdfminer.six==20201018",
    "requests==2.26.0",
]

GOOGLE_CLOUD_REQS = [
    "google-auth==2.2.1",
    "google-cloud-pubsub==2.8.0",
]

LINTING_REQS = [
    "black==21.6b0",
    "mypy==0.910",
    "types-requests==0.1",
]

TESTING_REQS = [
    "pytest>=6.2.2",
    "pytest-cov>=2.11.1",
]


setup(
    name=NAME,
    version=VERSION,
    description=INFO,
    author=AUTHORS,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=INSTALLATION_REQS,
    extras_require={
        "gcp": GOOGLE_CLOUD_REQS,
        "lint": LINTING_REQS,
        "test": TESTING_REQS,
        "all": [
            *GOOGLE_CLOUD_REQS,
            *LINTING_REQS,
            *TESTING_REQS,
        ],
    },
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass={},
)
