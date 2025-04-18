.PHONY: default all \
	install install-dev \
	download-ta-lib download-ta-lib-ci sparse-checkout \
	compile format lint \
	test coverage coverage-html docs badge \
	docker docker-ci docker-login \
	check-ta-lib check-env \
	migrate \
	setup-env

PROJECT_NAME ?= $(shell sed -n 's/^name = "\(.*\)"/\1/p' pyproject.toml)
APP_NAME ?= "algobosol"
APP_FILE ?= app.py
DOCKER_APP_IMAGE_TAG ?= "$(PROJECT_NAME)"

export AUTH_TOKEN ?= $(or $(GITLAB_ACCESS_TOKEN),$(CI_JOB_TOKEN))
export TA_LIB_URL := "https://gitlab.com/api/v4/projects/36396799/repository/files/ta-lib%2Fta-lib-0.4.0-src.tar.gz/raw?ref=main"
export TA_LIB_DEST ?= src.tar.gz
ifndef CI_REGISTRY_IMAGE
	CI_REGISTRY_IMAGE := "algobosol"
endif

default: all

install:
	@poetry install --only main --no-root

install-dev:
	@poetry install --no-root

download-ta-lib: check-env
	@curl --request GET \
		--header "PRIVATE-TOKEN: ${AUTH_TOKEN}" \
		--output ${TA_LIB_DEST} ${TA_LIB_URL}
	@tar -xf ${TA_LIB_DEST}

download-ta-lib-ci: sparse-checkout
	@tar -xf $(shell find algobosol/ta-lib -name '*.tar.gz' -type f)

compile:
	@poetry run python -m compileall $(APP_NAME)

format:
	@poetry run black --preview .
	@poetry run ruff check --fix .

lint:
	@poetry run black --preview --check .
	@poetry run ruff check --show-files .
	@poetry run mypy .

test:
	@poetry run \
		python -m pytest -v \
		--junitxml=public/test/junit.xml \
		--html=public/test/report.html

coverage:
	@poetry run coverage run -m pytest
	@poetry run coverage combine
	@poetry run coverage report

coverage-html:
	@poetry run coverage html

badge:
	@poetry run \
		genbadge tests \
		--input-file public/test/junit.xml \
		--output-file public/tests.svg
	@VERSION=$(shell poetry run python -m $(APP_NAME) docs version); \
	poetry run \
		anybadge \
		-l docs \
		-v $$VERSION \
		-f public/docs.svg \
		-c green

docs:
	@poetry run python -m $(APP_NAME) docs generate

run:
	@poetry run streamlit run $(APP_FILE)	

restart:
	@echo "🔄 Restarting Streamlit on port 8501..."
	@PID=$$(lsof -ti :8501); \
	if [ -n "$$PID" ]; then \
		echo "⚠️  Killing process on port 8501 (PID: $$PID)"; \
		kill -9 $$PID; \
	else \
		echo "✅ No process using port 8501"; \
	fi
	@nohup poetry run streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
	@echo "🚀 Streamlit restarted and running in background on port 8501"

collect:
	@poetry run python -m $(APP_NAME) collect

celery:
	@poetry run python -m $(APP_NAME) server celery --queue backtesting

all: install-dev test

check-ta-lib:
ifeq ($(shell ls ta-lib 2>/dev/null),)
	$(error You have to download ta-lib to the project directory (Run `make download-ta-lib`).)
endif

check-env:
ifeq ($(AUTH_TOKEN),)
	$(error 'GITLAB_ACCESS_TOKEN' is not defined.)
endif

setup-env:
	@echo "🔍 Detecting OS..."
	@unameOut=$$(uname -s); \
	case $$unameOut in \
		Darwin*)  \
			echo "🖥 Detected macOS"; \
			PYTHON_PATH="/opt/homebrew/bin/python3"; \
			if [ ! -f $$PYTHON_PATH ]; then \
				echo "❌ $$PYTHON_PATH not found. Please install Python via Homebrew."; \
				exit 1; \
			fi; \
			poetry env use $$PYTHON_PATH; \
			;; \
		Linux*)   \
			echo "🐧 Detected Linux"; \
			PYTHON_PATH=$$(which python3); \
			if [ -z $$PYTHON_PATH ]; then \
				echo "❌ python3 not found. Please install it via apt."; \
				exit 1; \
			fi; \
			poetry env use $$PYTHON_PATH; \
			;; \
		*)        \
			echo "❌ Unsupported OS"; \
			exit 1; \
	esac; \
	echo "✅ Python environment set to: $$PYTHON_PATH"; \
	poetry install
