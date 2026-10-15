.PHONY: format lint type typecheck test tests help lint_package

.DEFAULT_GOAL := help

.EXPORT_ALL_VARIABLES:
UV_FROZEN = true

######################
# TESTING
######################

TEST_FILE ?= tests/unit_tests/
PYTEST_EXTRA ?=

test: ## Run unit tests
test tests:
	uv run --group test pytest -vvv $(PYTEST_EXTRA) --disable-socket --allow-unix-socket $(TEST_FILE)

######################
# LINTING AND FORMATTING
######################

PYTHON_FILES=.
lint format: PYTHON_FILES=.
lint_package: ## Lint only the package
lint_package: PYTHON_FILES=ultragent

lint: ## Run linters and type checker
lint lint_package:
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff check $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff format $(PYTHON_FILES) --diff
	$(MAKE) type

type: ## Run type checker
type typecheck:
	uv run --all-groups ty check ultragent

format: ## Run code formatters
format:
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff format $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff check --fix $(PYTHON_FILES)

######################
# HELP
######################

help: ## Show this help message
	@echo "Usage: make [target] [TEST_FILE=path/to/tests/]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
