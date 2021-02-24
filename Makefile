PKG_VERSION   = $(shell cat VERSION)
COV_CONFIG    = ".coveragerc"
SOURCE_FOLDER = "src"
TESTS_FOLDER  = "tests"
TESTS_PARAMS  = "-p no:cacheprovider"
TYPING_PARAMS = "--allow-redefinition --ignore-missing-imports --cache-dir=/dev/null"


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER)
	@black --check $(TESTS_FOLDER)
	@echo "Checking type annotations"
	@mypy "$(TYPING_PARAMS)" $(SOURCE_FOLDER)
	@mypy "$(TYPING_PARAMS)" $(TESTS_FOLDER)


.PHONY: tag
tag:
	@echo "Tagging current commit"
	@git tag --annotate "v$(PKG_VERSION)" --message "Tag v$(PKG_VERSION)"
	@git push --follow-tags


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) "$(TESTS_PARAMS)"
