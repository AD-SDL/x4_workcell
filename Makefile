# Python Configuration
PYPROJECT_TOML := x4_app/pyproject.toml
PROJECT_VERSION := $(shell grep -oP '(?<=version = ")[^"]+' $(PYPROJECT_TOML) | head -n 1)

.DEFAULT_GOAL := init

.PHONY += init paths checks test clean
init: # Do the initial configuration of the project
	@test -e .env || cp example.env .env
	@sed -i 's/^USER_ID=.*/USER_ID=$(shell id -u)/' .env
	@sed -i 's/^GROUP_ID=.*/GROUP_ID=$(shell id -g)/' .env
	@sed -i 's/^PROJECT_VERSION=.*/PROJECT_VERSION=$(PROJECT_VERSION)/' .env
	@sed -i 's/^PROJECT_PATH=.*/PROJECT_PATH=$(shell pwd | sed 's/\//\\\//g')/' .env

.env: init

paths: .env # Create the necessary data directories
	@mkdir -p $(shell grep -E '^WEI_DATA_DIR=' .env | cut -d '=' -f 2)
	@mkdir -p $(shell grep -E '^REDIS_DIR=' .env | cut -d '=' -f 2)

checks: # Runs all the pre-commit checks
	@pre-commit install
	@pre-commit run --all-files || { echo "Checking fixes\n" ; pre-commit run --all-files; }

clean:
	@rm .env
