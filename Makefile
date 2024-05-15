.DEFAULT_GOAL := run

VENV ?= .venv
PYTHON ?= python3
PIP ?= pip3

JUNIT_OUTPUT := $(CURDIR)/output/junit-test_ansible_otel.xml

## @help:virtualenv:Create a Python virtual environment.
.PHONY: virtualenv
virtualenv:
	$(PYTHON) --version
	test -d $(VENV) || virtualenv -q --python=$(PYTHON) $(VENV);\
	source $(VENV)/bin/activate;\
	$(PIP) install -r requirements.txt;

## @help:run-test:Run the generated playbook.
.PHONY: run-test
run-test:
	source $(VENV)/bin/activate; \
	ANSIBLE_OPENTELEMETRY_TEST_GENERATE_OUTPUT_FILE=true \
	ansible-playbook playbook.yml

## @help:unit:Run the unit tests.
.PHONY: unit
unit:
	source $(VENV)/bin/activate; \
	$(PYTHON) -m pytest --capture=no --junitxml $(JUNIT_OUTPUT) test_pytest.py

## @help:test-it:Run the generated playbook in ITs.
.PHONY: test-it
test-it:
	source $(VENV)/bin/activate; \
	OTEL_EXPORTER_OTLP_INSECURE=true \
	OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4317 \
	ansible-playbook playbook.yml
