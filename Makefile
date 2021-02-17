PKG_VERSION   = $(shell cat VERSION)
COV_CONFIG    = ".coveragerc"
SOURCE_FOLDER = "src"
TESTS_PARAMS  = "-p no:cacheprovider"


.PHONY: tag
tag:
	@echo "Tagging current commit"
	@git tag --annotate "v$(PKG_VERSION)" --message "Tag v$(PKG_VERSION)"
	@git push --follow-tags


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) "$(TESTS_PARAMS)"
