# Dialect map I/O

### About
This repository contains the Input / Output capabilities to be used in data-ingestion jobs.

It will be used as a Python dependency in a small variety of data-ingestion pipelines
(_static-data_, _NLP metrics_...), in order to send curated information to the Dialect Map database,
making use of the private [Dialect map API][dialect-map-api-private].


### Dependencies
Python dependencies are specified within the `setup.py` file.

In order to install the development packages, as long as the defined commit hooks:
```sh
pip install ".[dev]"
pre-commit install
```


### Formatting
All Python files are formatted using [Black][black-web], and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```

In addition to the common _unit-tests_, there are specific groups of tests that require
non Python tools to be installed first. Those tests have been _marked_ using Pytest so that
they are not run by default.

The complete list of _markers_ is defined within the [pyproject.toml][pyproject-file] file.

To run a particular group of tests, set the `TESTS_MARKERS` environment variable to the name
of the desirable _marked group_ to run, or set it empty for full execution. Example:
```sh
export TESTS_MARKERS=""
make test
```


### Tagging
Commits can be tagged to create _informal_ releases of the package. In order to do so:

1. Bump up the package version (`VERSION`) following [Semantic Versioning][semantic-web].
2. Create and push a tag: `make tag`.


[black-web]: https://black.readthedocs.io/en/stable/
[dialect-map-api-private]: https://github.com/dialect-map/dialect-map-private-api
[dialect-map-main]: https://github.com/dialect-map/dialect-map
[pyproject-file]: pyproject.toml
[pytest-web]: https://docs.pytest.org/en/latest/#
[semantic-web]: https://semver.org/
