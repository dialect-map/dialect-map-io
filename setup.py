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


# Installation requirements
INSTALLATION_REQS = [
    "feedparser==6.0.2",
    "google-auth==1.24.0",
    "pdfminer.six==20201018",
    "requests==2.25.1",
]

# Development requirements
DEVELOPMENT_REQS = [
    "black>=20.8b1",
    "coverage>=5.0.4",
    "mypy==0.800",
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
    include_package_data=True,
    install_requires=INSTALLATION_REQS,
    extras_require={
        "dev": DEVELOPMENT_REQS,
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
