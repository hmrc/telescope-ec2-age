SHELL := /usr/bin/env bash
PWD = $(shell pwd)

default: help

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

docker-build-py35: ## Build the Python 3.5 container
	@docker build -t telemetry/telescope-ec2-age:latest .
.PHONY: docker-build-py35

test-py35-local: ## Run tests in a Python 3.5 container with a mounted volume (local)
	@docker run -v $(PWD):/app --rm telemetry/telescope-ec2-age poetry run pytest --cov=telemetry
.PHONY: test-py35

test-py35-ci: ## Run tests in a Python 3.5 container (CI)
	@docker run --rm telemetry/telescope-ec2-age poetry run pytest --cov=telemetry
.PHONY: test-ci

poetry-update: ## Update the dependencies as according to the pyproject.toml file
	poetry update -vvv
.PHONY: update

setup: docker-build-py35 ## Install local Poetry dependencies and build the Python 3.5 image
	poetry install -vvv
	poetry export -f requirements.txt > requirements.txt
.PHONY: setup