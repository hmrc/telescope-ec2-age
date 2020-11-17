SHELL := /usr/bin/env bash
PWD = $(shell pwd)

default: help

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

build-py3.5: ## Build the Python 3.5 container
	@docker build -t telemetry/telescope-ec2-age:latest .
.PHONY: build-py3.5

test-py3.5-local: ## Run tests in a Python 3.5 container
	@docker run --rm telemetry/telescope-ec2-age -v $(PWD):/app
.PHONY: test-py3.5

test-py3.5-ci:
	@docker run --rm telemetry/telescope-ec2-age
.PHONY: test-ci
