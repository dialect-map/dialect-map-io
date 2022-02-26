PKG_VERSION   = $(shell cat VERSION)
COV_CONFIG    = ".coveragerc"
SOURCE_FOLDER = "src"
TESTS_FOLDER  = "tests"
TESTS_PARAMS  = "-p no:cacheprovider --strict-markers"

# Configurable options
TESTS_MARKERS ?= "'not gcp'"


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER) $(TESTS_FOLDER)
	@isort --check $(SOURCE_FOLDER) $(TESTS_FOLDER)
	@mypy --pretty $(SOURCE_FOLDER) $(TESTS_FOLDER)


.PHONY: tag
tag:
	@echo "Tagging current commit"
	@git tag --annotate "v$(PKG_VERSION)" --message "Tag v$(PKG_VERSION)"
	@git push --follow-tags


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) -m "$(TESTS_MARKERS)" "$(TESTS_PARAMS)"
