SHELL := /usr/bin/env bash
PWD = $(shell pwd)

DOCKER_AWS_VARS = -e AWS_REGION=${AWS_REGION} -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

default: help

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

build: docker-build-py35 ## Install local Poetry dependencies and build the Python 3.5 image
	@poetry install -vvv
	@poetry export -f requirements.txt > requirements.txt
	$(MAKE) poetry-build
.PHONY: setup

docker-build-py35: ## Build the Python 3.5 container
	@docker build -t telemetry/telescope-ec2-age:latest .
.PHONY: docker-build-py35

poetry-build: ## Builds a tarball and a wheel Python packages
	@poetry build
.PHONY: poetry-build

poetry-update: ## Update the dependencies as according to the pyproject.toml file
	@poetry update -vvv
.PHONY: update

run-py35: ## Run the telescope-ec2-age application in a Python 3.5 container
	@docker run ${DOCKER_AWS_VARS} -v $(PWD):/app --rm telemetry/telescope-ec2-age python bin/telescope-ec2-age.py
.PHONY: run-py35

sh-py35: ## Get a shell in a Python 3.5 container
	@docker run ${DOCKER_AWS_VARS} -it -v $(PWD):/app --rm telemetry/telescope-ec2-age bash
.PHONY: sh-py35