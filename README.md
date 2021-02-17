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


### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```


### Tagging
Commits can be tagged to create _informal_ releases of the package. In order to do so:

1. Bump up the package version (`VERSION`) following [Semantic Versioning][semantic-web].
2. Create and push a tag: `make tag`.


[dialect-map-api-private]: https://github.com/dialect-map/dialect-map-private-api
[dialect-map-main]: https://github.com/dialect-map/dialect-map
[pytest-web]: https://docs.pytest.org/en/latest/#
[semantic-web]: https://semver.org/
