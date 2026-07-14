.PHONY: install install-dev audit build serve clean

PYTHON ?= python
PIP ?= $(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

audit:
	$(PYTHON) scripts/audit_docs.py

build:
	$(PYTHON) -m mkdocs build --strict

serve:
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf site
